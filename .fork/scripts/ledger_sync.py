# ruff: noqa: INP001 - a script run by path, not a module of any package.

"""Compare upstream's pull requests and issues with `.fork/ledger.json`.

It reports what changed upstream since the ledger was last touched: new items, pull requests whose
head moved after they were seen, items upstream merged or closed, and fork commits carrying an
`Upstream-PR` trailer whose pull request upstream merged, which the next rebase collapses, or
which the ledger does not know at all.

`--write` records the facts: new items go in as `pending`, `seen_head_sha` follows the head and
`upstream_merge_sha` and `upstream_closed` are set once upstream merges or closes. A decision (`status`, `reason`, `fork_commit`)
is never changed here; that stays a person's call, recorded by hand.

Run from the repository root. It needs `gh` signed in and the upstream branch fetched:

    git fetch upstream
    uv run python .fork/scripts/ledger_sync.py [--write] [--output report.md]
"""

from __future__ import annotations

import argparse
import json
import pathlib
import subprocess
import sys
from dataclasses import dataclass, field
from typing import Any

LEDGER = pathlib.Path(".fork/ledger.json")

# `gh pr list` stops at its limit silently, so the limit sits far above upstream's open count
#  and `fetch_open` refuses to go on when a page comes back full.
LIST_LIMIT = 500


def gh_json(*args: str) -> Any:
    out = subprocess.run(["gh", *args], check=True, capture_output=True, text=True).stdout
    return json.loads(out)


def git(*args: str) -> str:
    return subprocess.run(["git", *args], check=True, capture_output=True, text=True).stdout


def fetch_open(repository: str, kind: str, fields: str) -> dict[str, dict[str, Any]]:
    items = gh_json(kind, "list", "-R", repository, "--state", "open", "-L", str(LIST_LIMIT),
                    "--json", fields)  # fmt: skip

    if len(items) >= LIST_LIMIT:
        sys.exit(f"`gh {kind} list` returned {LIST_LIMIT} items, raise LIST_LIMIT")

    return {str(item["number"]): item for item in items}


def fetch_closed_pr(repository: str, number: str) -> dict[str, Any]:
    return gh_json("pr", "view", number, "-R", repository,
                   "--json", "state,headRefOid,mergeCommit,closedAt")  # fmt: skip


def fetch_closed_issue(repository: str, number: str) -> dict[str, Any]:
    return gh_json("issue", "view", number, "-R", repository, "--json", "state,closedAt")


def upstream_pr_trailers(upstream_ref: str, fork_ref: str) -> dict[str, list[str]]:
    """Map every `Upstream-PR` number on the fork's stack to the commits that carry it."""
    log = git("log", "--format=%h%x00%(trailers:key=Upstream-PR,valueonly,separator=%x2C)%x1e",
              f"{upstream_ref}..{fork_ref}")  # fmt: skip
    found: dict[str, list[str]] = {}

    for record in log.split("\x1e"):
        if not record.strip():
            continue

        sha, _, trailers = record.strip().partition("\x00")

        for value in trailers.split(","):
            number = value.strip().lstrip("#")
            if number:
                found.setdefault(number, []).append(sha)

    return found


@dataclass
class Report:
    new_prs: list[str] = field(default_factory=list)
    moved_prs: list[str] = field(default_factory=list)
    merged_prs: list[str] = field(default_factory=list)
    closed_prs: list[str] = field(default_factory=list)
    new_issues: list[str] = field(default_factory=list)
    closed_issues: list[str] = field(default_factory=list)
    collapsing: list[str] = field(default_factory=list)
    untracked: list[str] = field(default_factory=list)
    upstream_moved: list[str] = field(default_factory=list)

    def is_empty(self) -> bool:
        return not any(vars(self).values())

    def markdown(self) -> str:
        sections = [
            ("New upstream pull requests", self.new_prs),
            ("Pull requests whose head moved since it was seen", self.moved_prs),
            ("Pull requests upstream merged", self.merged_prs),
            ("Pull requests upstream closed without merging", self.closed_prs),
            ("New upstream issues", self.new_issues),
            ("Issues upstream closed", self.closed_issues),
            ("Fork commits the next rebase collapses", self.collapsing),
            ("Fork commits whose `Upstream-PR` has no ledger entry", self.untracked),
            ("Upstream commits not yet rebased onto", self.upstream_moved),
        ]
        lines = ["# Ledger sync", ""]

        if self.is_empty():
            lines.append("Nothing changed upstream since the ledger was last synced.")

        for title, entries in sections:
            if entries:
                lines += [f"## {title}", "", *(f"- {entry}" for entry in entries), ""]

        return "\n".join(lines).rstrip() + "\n"


def pr_entry(item: dict[str, Any]) -> dict[str, Any]:
    owner = (item.get("headRepositoryOwner") or {}).get("login", "?")
    return {
        "title": item["title"],
        "author": (item.get("author") or {}).get("login"),
        "head": f"{owner}:{item['headRefName']}",
        "reviewed_head_sha": None,
        "seen_head_sha": item["headRefOid"],
        "closes": [],
        "status": "pending",
        "fork_commit": None,
        "upstream_merge_sha": None,
        "reason": None,
        "notes": None,
    }


def sync_prs(ledger: dict[str, Any], repository: str, report: Report, write: bool) -> None:
    open_prs = fetch_open(repository, "pr",
                          "number,title,author,headRefName,headRepositoryOwner,headRefOid")  # fmt: skip
    known: dict[str, dict[str, Any]] = ledger["pull_requests"]

    for number, item in open_prs.items():
        entry = known.get(number)

        if entry is None:
            report.new_prs.append(f"#{number} {item['title']}")
            if write:
                known[number] = pr_entry(item)
            continue

        if entry["seen_head_sha"] != item["headRefOid"]:
            reviewed = entry.get("reviewed_head_sha")
            note = " (reviewed at the old head, re-review)" if reviewed else ""
            report.moved_prs.append(
                f"#{number} {entry['seen_head_sha'][:8]} -> {item['headRefOid'][:8]}{note}"
            )
            if write:
                entry["seen_head_sha"] = item["headRefOid"]

    for number, entry in known.items():
        if number in open_prs or entry.get("upstream_closed"):
            continue

        state = fetch_closed_pr(repository, number)
        merge: str | None = None

        if state["state"] == "MERGED":
            merge = state["mergeCommit"]["oid"]
            report.merged_prs.append(f"#{number} as {merge[:8]}, ledger status `{entry['status']}`")
        else:
            report.closed_prs.append(f"#{number}, ledger status `{entry['status']}`")

        if write:
            entry["upstream_merge_sha"] = merge
            entry["upstream_closed"] = state["closedAt"]


def sync_issues(ledger: dict[str, Any], repository: str, report: Report, write: bool) -> None:
    open_issues = fetch_open(repository, "issue", "number,title")
    known: dict[str, dict[str, Any]] = ledger["issues"]

    for number, item in open_issues.items():
        if number not in known:
            report.new_issues.append(f"#{number} {item['title']}")
            if write:
                known[number] = {
                    "title": item["title"],
                    "status": "pending",
                    "addressed_by": None,
                    "notes": None,
                }

    for number, entry in known.items():
        if number in open_issues or entry.get("upstream_closed"):
            continue

        state = fetch_closed_issue(repository, number)
        report.closed_issues.append(f"#{number}, ledger status `{entry['status']}`")

        if write:
            entry["upstream_closed"] = state["closedAt"]


def sync_stack(ledger: dict[str, Any], upstream_ref: str, fork_ref: str, report: Report) -> None:
    for number, commits in sorted(upstream_pr_trailers(upstream_ref, fork_ref).items()):
        entry = ledger["pull_requests"].get(number)

        if entry is None:
            report.untracked.append(f"#{number}: {', '.join(commits)}")
        elif entry.get("upstream_merge_sha"):
            report.collapsing.append(f"#{number}: {', '.join(commits)}")

    synced = ledger["last_synced_upstream_main"]
    report.upstream_moved = git("log", "--format=%h %s", f"{synced}..{upstream_ref}").splitlines()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--write", action="store_true", help="record the facts in the ledger")
    parser.add_argument("--output", type=pathlib.Path, help="also write the report here")
    parser.add_argument("--upstream-ref", default="upstream/main")
    parser.add_argument("--fork-ref", default="HEAD")
    args = parser.parse_args()

    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    repository = ledger["upstream"]
    report = Report()

    sync_prs(ledger, repository, report, args.write)
    sync_issues(ledger, repository, report, args.write)
    sync_stack(ledger, args.upstream_ref, args.fork_ref, report)

    text = report.markdown()
    sys.stdout.write(text)

    if args.output:
        args.output.write_text(text, encoding="utf-8")

    if args.write:
        dumped = json.dumps(ledger, indent=2, ensure_ascii=False) + "\n"
        LEDGER.write_text(dumped, encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
