# ruff: noqa: INP001 - a script run by path, not a module of any package.

"""Report how far the fork is from Telegram: schema layer, raw API wrappers and Bot API parity.

It writes `.fork/coverage.md` and compares three numbers with the ones saved in
`.fork/coverage.json`: the layers the schema is behind, the raw functions no high-level method
calls, and the Bot API names with no counterpart. It exits 1 when any of them grew. `--write`
saves the new numbers and the Bot API name list, which is what the next run diffs a new Bot API
release against.

Run from the repository root:

    uv run python .fork/scripts/coverage.py [--write] [--cached]

`--cached` reuses the pages fetched last time from `.fork/.cache/` instead of downloading them.
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import pathlib
import re
import sys
import urllib.request
from dataclasses import dataclass
from typing import Any

# The package supports 3.10, which has no `tomllib`; these scripts only ever run on a current one.
if sys.version_info >= (3, 11):
    import tomllib
else:
    sys.exit("coverage.py needs Python 3.11 or later")

FORK = pathlib.Path(".fork")
CACHE = FORK / ".cache"
STATE = FORK / "coverage.json"
REPORT = FORK / "coverage.md"

SCHEMA = pathlib.Path("compiler/api/source/main_api.tl")
TDESKTOP_SCHEMA = (
    "https://raw.githubusercontent.com/telegramdesktop/tdesktop/dev/"
    "Telegram/SourceFiles/mtproto/scheme/api.tl"
)
BOT_API = "https://core.telegram.org/bots/api"

# Written out by hand in our schema (`// Parsed manually`), so tdesktop is the only one that
#  declares them and they would otherwise always show as added.
BUILTIN_CONSTRUCTORS = frozenset({"boolFalse", "boolTrue", "true", "vector", "error", "null"})

TL_LINE = re.compile(r"^([\w.]+)#([0-9a-f]+)\s+(.*?)\s*=\s*([^;]+);")
LAYER_LINE = re.compile(r"^//\s*LAYER\s+(\d+)", re.MULTILINE)

RAW_REFERENCE = re.compile(r"raw\.functions\.(?:([a-z_]+)\.)?([A-Z]\w*)")
RAW_IMPORT = re.compile(r"from pyrogram\.raw\.functions(?:\.([a-z_]+))? import ([\w, ()\n]+)")

BOT_API_HEADING = re.compile(
    r'<h4><a class="anchor" name="[^"]+" href="#[^"]+"><i class="anchor-icon"></i></a>(\w+)</h4>'
)
BOT_API_VERSION = re.compile(r"Bot API (\d+\.\d+)")

METHOD_DEFINITION = re.compile(r"^\s+(?:async )?def ([a-z]\w*)\(\s*self", re.MULTILINE)
CLASS_DEFINITION = re.compile(r"^class ([A-Z]\w*)\(", re.MULTILINE)


def fetch(url: str, name: str, *, cached: bool) -> str:
    path = CACHE / name

    if cached and path.exists():
        return path.read_text(encoding="utf-8")

    request = urllib.request.Request(url, headers={"User-Agent": "kurigram-fork-coverage"})
    with urllib.request.urlopen(request, timeout=60) as response:
        text = response.read().decode("utf-8")

    CACHE.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return text


def parse_schema(text: str) -> tuple[int, dict[tuple[str, str], str]]:
    """Answer the layer and every combinator as `(section, name) -> normalized line`."""
    layer = LAYER_LINE.search(text)
    if layer is None:
        sys.exit("no `// LAYER` line in a schema")

    entries: dict[tuple[str, str], str] = {}
    section = "types"

    for raw_line in text.splitlines():
        line = raw_line.strip()

        if line.startswith("---"):
            section = line.strip("-")
            continue

        match = TL_LINE.match(line)
        if match and match[1] not in BUILTIN_CONSTRUCTORS:
            entries[section, match[1]] = " ".join(line.split())

    return int(layer[1]), entries


def class_name(function: str) -> tuple[str, str]:
    """`messages.sendMessage` -> `("messages", "SendMessage")`, the compiler's own rule."""
    namespace, _, name = function.rpartition(".")
    return namespace, name[0].upper() + name[1:]


def referenced_functions() -> set[tuple[str, str]]:
    found: set[tuple[str, str]] = set()

    for path in pathlib.Path("pyrogram").rglob("*.py"):
        if path.parts[1] == "raw":
            continue

        source = path.read_text(encoding="utf-8")
        found.update((namespace or "", name) for namespace, name in RAW_REFERENCE.findall(source))

        for namespace, names in RAW_IMPORT.findall(source):
            for name in re.findall(r"[A-Z]\w*", names):
                found.add((namespace or "", name))

    return found


def defined_names(root: str, pattern: re.Pattern[str]) -> set[str]:
    names: set[str] = set()
    for path in pathlib.Path(root).rglob("*.py"):
        names.update(pattern.findall(path.read_text(encoding="utf-8")))
    return names


def snake(name: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()


@dataclass
class Section:
    title: str
    lines: list[str]


def layer_drift(cached: bool) -> tuple[int, Section]:
    ours_layer, ours = parse_schema(SCHEMA.read_text(encoding="utf-8"))
    theirs_layer, theirs = parse_schema(fetch(TDESKTOP_SCHEMA, "tdesktop_api.tl", cached=cached))

    added = sorted(key for key in theirs if key not in ours)
    removed = sorted(key for key in ours if key not in theirs)
    changed = sorted(key for key in ours if key in theirs and ours[key] != theirs[key])

    lines = [f"Our schema: layer {ours_layer}. tdesktop `dev`: layer {theirs_layer}.", ""]

    if not (added or removed or changed):
        lines.append("Every combinator matches.")

    for title, keys in (("Added", added), ("Removed", removed), ("Changed", changed)):
        if keys:
            lines += [f"**{title}** ({len(keys)}):", ""]
            lines += [f"- `{name}` ({section})" for section, name in keys]
            lines.append("")

    return max(theirs_layer - ours_layer, 0), Section("Layer drift", lines)


def raw_coverage() -> tuple[int, Section]:
    ignore = tomllib.loads((FORK / "coverage_ignore.toml").read_text(encoding="utf-8"))
    patterns: list[str] = ignore["ignore"]

    _, schema = parse_schema(SCHEMA.read_text(encoding="utf-8"))
    functions = sorted(name for section, name in schema if section == "functions")
    called = referenced_functions()

    gaps: dict[str, list[str]] = {}
    totals: dict[str, int] = {}

    for function in functions:
        if any(fnmatch.fnmatchcase(function, pattern) for pattern in patterns):
            continue

        namespace, name = class_name(function)
        label = namespace or "(top level)"
        totals[label] = totals.get(label, 0) + 1

        if (namespace, name) not in called:
            gaps.setdefault(label, []).append(function)

    unwrapped = sum(len(names) for names in gaps.values())
    tracked = sum(totals.values())

    lines = [
        (
            f"{tracked - unwrapped} of {tracked} tracked raw functions are called by a high-level "
            f"method; {unwrapped} are not. `coverage_ignore.toml` leaves out the ones that should "
            "never get a wrapper."
        ),
        "",
        "| Namespace | Unwrapped | Tracked |",
        "|-----------|-----------|---------|",
    ]
    lines += [
        f"| {label} | {len(gaps.get(label, []))} | {total} |"
        for label, total in sorted(totals.items(), key=lambda item: -len(gaps.get(item[0], [])))
    ]
    lines.append("")

    for label, names in sorted(gaps.items()):
        lines += [f"<details><summary>{label} ({len(names)})</summary>", ""]
        lines += [f"- `{name}`" for name in names]
        lines += ["", "</details>", ""]

    return unwrapped, Section("Raw API coverage", lines)


def bot_api_parity(cached: bool, previous: dict[str, Any]) -> tuple[int, dict[str, Any], Section]:
    html = fetch(BOT_API, "bot_api.html", cached=cached)
    version = BOT_API_VERSION.search(html)
    if version is None:
        sys.exit("no `Bot API N.N` on the Bot API page")

    # The headings before "Getting updates" are changelog dates and prose, never a name.
    names = BOT_API_HEADING.findall(html[html.index('name="getting-updates"') :])
    methods = sorted({name for name in names if name[0].islower()})
    types = sorted({name for name in names if name[0].isupper()})

    aliases = tomllib.loads((FORK / "bot_api_aliases.toml").read_text(encoding="utf-8"))
    accounted = {
        kind: {**aliases[kind]["renamed"], **aliases[kind]["not_applicable"],
               **aliases[kind]["different_shape"]}
        for kind in ("methods", "types")
    }  # fmt: skip

    our_methods = defined_names("pyrogram/methods", METHOD_DEFINITION)
    our_types = defined_names("pyrogram/types", CLASS_DEFINITION)

    method_gaps = [
        m for m in methods if snake(m) not in our_methods and m not in accounted["methods"]
    ]
    type_gaps = [t for t in types if t not in our_types and t not in accounted["types"]]

    stale = [
        f"`{name}` -> `{target}`"
        for name, target in aliases["methods"]["renamed"].items()
        if target not in our_methods
    ] + [
        f"`{name}` -> `{target}`"
        for name, target in aliases["types"]["renamed"].items()
        if target not in our_types
    ]

    lines = [
        (
            f"Bot API {version[1]}: {len(methods)} methods, {len(types)} types. "
            f"{len(method_gaps)} methods and {len(type_gaps)} types have no counterpart here."
        ),
        "",
    ]

    if previous.get("bot_api_version") and previous["bot_api_version"] != version[1]:
        new_methods = sorted(set(methods) - set(previous.get("bot_api_methods", [])))
        new_types = sorted(set(types) - set(previous.get("bot_api_types", [])))
        lines += [f"**New since Bot API {previous['bot_api_version']}:**", ""]
        lines += [f"- `{name}`" for name in new_methods + new_types] or ["- nothing"]
        lines.append("")

    if stale:
        lines += ["**Aliases pointing at a name that no longer exists:**", ""]
        lines += [f"- {entry}" for entry in stale]
        lines.append("")

    for title, gaps in (("Methods", method_gaps), ("Types", type_gaps)):
        lines += [f"<details><summary>{title} ({len(gaps)})</summary>", ""]
        lines += [f"- `{name}`" for name in gaps]
        lines += ["", "</details>", ""]

    snapshot = {"bot_api_version": version[1], "bot_api_methods": methods, "bot_api_types": types}
    return (
        len(method_gaps) + len(type_gaps) + len(stale),
        snapshot,
        Section("Bot API parity", lines),
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--write", action="store_true", help="save the numbers as the new baseline")
    parser.add_argument("--cached", action="store_true", help="reuse the pages in .fork/.cache")
    args = parser.parse_args()

    previous: dict[str, Any] = (
        json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else {}
    )

    layers_behind, drift = layer_drift(args.cached)
    unwrapped, raw = raw_coverage()
    bot_api_gaps, snapshot, parity = bot_api_parity(args.cached, previous)

    numbers = {
        "layers_behind": layers_behind,
        "raw_unwrapped": unwrapped,
        "bot_api_gaps": bot_api_gaps,
    }
    baseline: dict[str, int] = previous.get("numbers", {})
    worse = [key for key, value in numbers.items() if key in baseline and value > baseline[key]]

    lines = ["# Fork coverage", "", "| Number | Now | Baseline |", "|--------|-----|----------|"]
    lines += [f"| `{key}` | {value} | {baseline.get(key, '-')} |" for key, value in numbers.items()]
    lines.append("")

    for section in (drift, raw, parity):
        lines += [f"## {section.title}", "", *section.lines, ""]

    text = "\n".join(lines).rstrip() + "\n"
    REPORT.write_text(text, encoding="utf-8", newline="\n")
    sys.stdout.write(text)

    if args.write:
        state = {"numbers": numbers, **snapshot}
        STATE.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8", newline="\n")
    elif worse:
        sys.exit(f"worse than the baseline: {', '.join(worse)}")


if __name__ == "__main__":
    main()
