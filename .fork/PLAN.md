# Fork maintenance plan

This fork (`Alb0204/kurigram`) tracks [`kurigram-org/kurigram`](https://github.com/kurigram-org/kurigram).
It is not a rival project. Its goal is to ship upstream's pending fixes, plus features upstream
hasn't reached yet, sooner than upstream does, while staying close enough that syncing stays cheap.
Everything under `.fork/` is fork-only.

**Rule: this fork only reads from upstream.** No pushes, PRs, issues or comments go to
`kurigram-org/kurigram`. Both clones have `upstream`'s push URL set to `DISABLED-fork-only`, and
`gh repo set-default` points at the fork. Pass `-R Alb0204/kurigram` to every `gh pr`/`gh issue`
command anyway, because `gh` targets a fork's parent by default.

- `PLAN.md`: this file, covering how the fork is run. Change it when the process changes.
- `ledger.json`: every upstream PR, issue and branch reviewed so far, with its decision. Update it
  in the same commit as the work it records.
- `DECISIONS.md`: one dated line per non-obvious call (ours versus theirs, rejections), newest first.

## 0. Starting point (2026-10-28)

- Fork `main` was identical to `upstream/main` at `80aa42d4`. The fork has no changes of its own yet.
- **The 26 extra branches on `origin` are not fork work.** They are byte-identical copies of
  upstream's own branches, which back upstream's open PRs #520–#553 (mostly by Danipulok) and one
  dependabot PR. One branch, `fix/edit-message-reply-markup-removal`, has no PR at all. "Check the
  branches and merge them" therefore means "adopt upstream's pending PRs early", which is what §3
  does.
- Upstream has 36 open PRs and 13 open issues. All of them are seeded in `ledger.json` as `pending`.
- Stacking: `test/markdown-round-trip-corpus` (#552) contains every commit of `refactor/parser`
  (#549). No other open branch contains another one.
- API layer: 232 in `compiler/api/source/main_api.tl`, the same as tdesktop's current schema.
  Upstream bumps layers within days (230 → 231 → 232 between 2026-10-09 and 2026-10-21), so layer
  bumps are not where the fork gets ahead. Wrapping what the layer already exposes is.
- Coverage baseline, from a prototype run of the §6 script:
  - Raw TL functions: 336 of 859 are called from a high-level method (39%). The largest gaps are
    `messages` (141 unwrapped), `account` (96), `phone` (42), `payments` (40), `channels` (24),
    `bots` (24) and `wallet` (23).
  - Bot API 10.3: 124 of 185 methods match a `Client` method by name. Most of the other 61 are
    naming differences (`getMyCommands` versus `get_bot_commands`, `forwardMessage` versus
    `forward_messages`) or don't apply to MTProto (`getUpdates`, `setWebhook`). That is what the
    alias file in §6 sorts out.

## 1. Repository model

Remotes: `origin` is `Alb0204/kurigram` and `upstream` is `kurigram-org/kurigram`. Fetch both with
`git fetch --all --prune` at the start of every session.

**Integration model: a linear stack on top of upstream** (confirmed by the owner, 2026-10-28).

- Fork `main` is `upstream/main` plus a stack of fork commits. The first commit adds `.fork/`. Each
  later commit is one adopted PR or one fork-only change.
- Every adopted commit carries a trailer, `Upstream-PR: #NNN` or `Fork-only: <slug>`, so scripts can
  map commits back to ledger entries.
- To sync, run `git rebase upstream/main`. Git drops a commit whose patch upstream has already
  merged. Upstream squash-merges PRs (`(#531)`, `(#560)`), so the squashed result usually differs
  from the PR's commits and the rebase stops with a conflict on it. That conflict is the
  "upstream merged it" signal §4 handles.
- After each sync, force-push `main` with `--force-with-lease`. Tag the pre-sync tip as
  `fork-sync/YYYY-MM-DD` first, so anything pinned to an old SHA can still resolve it.

This model was chosen because upstream squash-merges. With a merge-based model, every upstream
squash of a PR the fork already adopted produces a duplicate or a conflict on every later sync, and
the history stops showing which fork commits are still fork-only. If force-pushing `main` is
unacceptable, for example because other projects pin fork SHAs without tags, switch to merging
`upstream/main` into `main`. The ledger still works; only §4's conflict handling becomes manual.

Branch naming follows upstream's style (`fix/…`, `feat/…`, `docs/…`, `refactor/…`, `test/…`,
`ci/…`, `chore/…`). A branch adopted from an upstream PR keeps the PR's branch name so the two are
easy to correlate.

## 2. Tracking rules

`ledger.json` is the single source of truth for "have we looked at this already?".

- **Keys.** PRs are keyed by number and record `seen_head_sha`, the head when last listed, and
  `reviewed_head_sha`, the head that was actually reviewed. A PR needs another look only when
  upstream's current `headRefOid` differs from `reviewed_head_sha`, or when its status is
  `pending`.
- **Statuses:**
  - `pending`: not reviewed yet.
  - `adopted`: merged into the fork; `fork_commit` set.
  - `deferred`: reviewed, but its intended feature isn't complete yet. It stays open, and `reason`
    says what's missing.
  - `rejected`: won't be adopted; `reason` set.
  - `superseded`: upstream merged it or something better, so the fork's copy is dropped and
    `upstream_merge_sha` is set.
  - `fork-only`: a fork change with no upstream counterpart.
- **Issues** record `addressed_by`, the PRs or fork commits that fix them.
- `last_synced_upstream_main` advances on every sync.
- `DECISIONS.md` gets one line whenever a choice isn't obvious from the status alone. Examples: "kept
  ours over upstream #NNN because …", "rejected #NNN: duplicates #MMM", "deferred #NNN: no test for
  the channel case yet".

**Every session:**

1. `git fetch --all --prune`.
2. Run the ledger diff (§6, `ledger_sync.py`). It lists new PRs and issues, PRs whose head moved,
   PRs and issues upstream closed or merged, and fork commits whose trailer has no ledger entry.
3. Work the list from step 2 before starting new feature work.
4. Before pushing, run `make api && make lint && make typecheck && make test-unit`, then commit the
   ledger changes together with the work they describe.

## 3. Phase 1: triage upstream's open PRs

**Per-PR procedure:**

1. Read the PR description, its linked issue and the upstream review comments. A maintainer
   objection is a reason to defer, not to adopt anyway.
2. Rebase the PR onto fork `main` in a local branch. External-fork PRs are fetched with
   `git fetch upstream pull/NNN/head:pr/NNN`.
3. Check that the PR actually does what its title and description say:
   - Read the diff against the claim.
   - Confirm there is a test that fails without the change and passes with it.
   - Run the full gate: `make api && make lint && make typecheck && make test-unit`.
4. Decide:
   - Correct and complete: `adopted`. Fast-forward it onto `main` as its own commit(s) with the
     `Upstream-PR` trailer.
   - Correct direction but incomplete or wrong in places: `deferred`. Optionally finish it on a
     fork branch. The entry then notes "fork carries fixes on top" and becomes `adopted` once the
     finished version lands.
   - Wrong, or made obsolete by another PR: `rejected`.
5. Record `reviewed_head_sha`, the status and the reason in `ledger.json`.

**Order.** Cheap and independent PRs go first, so `main` gains value quickly and later rebases have
less to carry.

1. CI, deps and docs: #553 (urllib3), #534 (pin actions), #539 (sphinx `-W`), #536, #538, #540,
   #535, #537 (#537 adds a guard test, so run it last in this group).
2. Small type fixes: #547, #546, #542, #545, #544, #543, #548, #533.
3. Behaviour fixes with linked issues: #557 (#526), #525 (#524), #556 (#331), #555, #541, #532,
   `fix/edit-message-reply-markup-removal` (no PR; 76 commits behind, so rebase first).
4. Large refactors, one at a time, re-running the whole suite after each: #521, #550, #551, then
   #549 followed by #552, which is stacked on #549.
5. Features from outside contributors, which need the closest look: #520 (41 behind; closes #174),
   #527 and #488 (both touch `min` peer resolution, #478, so pick one), #523, #558, #559, #479,
   #450, #471.

The 26 copies of upstream branches on `origin` were deleted on 2026-10-28, after their head SHAs
went into the ledger (`seen_head_sha`). Upstream still holds the originals, and
`git fetch upstream` brings them back locally whenever a review needs one. `origin` carries only
`main`, fork work branches and the fork's own tags from now on.

## 4. Phase 2: keep in step with upstream

Run this whenever `upstream/main` moves, which `ledger_sync.py` reports.

1. Tag the current tip `fork-sync/YYYY-MM-DD`, then `git rebase upstream/main`.
2. For each fork commit, the rebase either:
   - **drops it**, because upstream has the identical patch. Mark the entry `superseded` and set
     `upstream_merge_sha`;
   - **applies it cleanly**. It is still fork-only, so nothing changes;
   - **conflicts**, which almost always means upstream squash-merged or reworked the same PR.
     Compare the two versions:
     - **Theirs is equivalent or better:** skip our commit (`git rebase --skip`) and mark the entry
       `superseded`.
     - **Ours is better** (fixes a case theirs misses, or has a test theirs lacks): keep ours,
       rewritten on top of theirs as a small delta commit with a `Fork-only:` trailer, and add a
       `DECISIONS.md` line saying why.
     - **Both differ in non-overlapping ways:** merge them by hand and record that in
       `DECISIONS.md`.
3. Run the full gate, update `last_synced_upstream_main`, then force-push with lease.

Upstream PRs that were closed without merging keep the fork's adopted copy. The ledger keeps the
`adopted` status, and `DECISIONS.md` notes that upstream declined the PR and why the fork kept it.

## 5. Phase 3: open upstream issues

Issues go through the same ledger flow as PRs:

- An issue with a PR (#526, #524, #478, #331, #174, #143) is resolved when that PR is adopted.
- An issue without a PR (#202, #160, #224, #62) needs a reproduction first. Only after that does
  the fork write a fix of its own as a `Fork-only` commit.
- Discussions (#438, #109) and the module rename (#150) are tracked for their outcome only. The
  fork follows upstream on naming and never leads, because a rename breaks every import.

## 6. Automation (`.fork/scripts/`)

Both scripts are plain Python that run offline against the repo, plus network fetches that are
cached. They need to pass `ruff` and `ty`, and must not trip `tests/guards`, which sweeps the whole
repository. Check that with `make test-guards` before committing them.

Built 2026-10-29. Run them from the repository root:

```
git fetch upstream
uv run python .fork/scripts/ledger_sync.py           # report only
uv run python .fork/scripts/ledger_sync.py --write   # also record new items and moved heads
uv run python .fork/scripts/coverage.py              # writes .fork/coverage.md
uv run python .fork/scripts/coverage.py --write      # also saves the numbers as the baseline
```

`coverage.py --cached` reuses the pages in `.fork/.cache/` (git-ignored). The baseline lives in
`.fork/coverage.json`. Move it with `--write` only in the same commit as the change that moved
the numbers, so every jump in the history has a reason next to it.

### `ledger_sync.py` (do first, it's the smaller one)

1. Pull open and recently closed PRs and issues via `gh` (`gh pr list --state all --json …`).
2. Diff them against `ledger.json` and print:
   - new items;
   - items whose head SHA moved;
   - items upstream merged or closed;
   - fork commits with an `Upstream-PR` trailer whose PR upstream merged, which the next rebase
     will collapse.
3. With `--write`, add new items as `pending` and refresh `seen_head_sha`. It never changes a
   decision on its own.

### `coverage.py`

It writes `.fork/coverage.md` with three sections and exits non-zero only when a tracked number
gets worse.

1. **Layer drift.** Compare the `// LAYER N` line in `compiler/api/source/main_api.tl` with
   tdesktop's `Telegram/SourceFiles/mtproto/scheme/api.tl` on `dev`. If tdesktop is ahead, list the
   constructors and functions added, removed or changed in signature. This is the early warning
   for a schema bump.
2. **Raw API coverage.** Parse `---functions---` from `main_api.tl`. Collect every
   `raw.functions.<ns>.<Name>` referenced under `pyrogram/`, excluding `pyrogram/raw/`. Report the
   unwrapped functions per namespace. A curated `coverage_ignore.toml` lists functions that
   shouldn't get a high-level wrapper (`help.*` internals, `auth.*` handled by `Client`, `test.*`),
   so the number tracks real gaps only.
3. **Bot API parity.** Scrape the `<h4>` method and type names from
   `https://core.telegram.org/bots/api`, recording the version (currently 10.3). Map methods to
   `snake_case` and types to class names. A `bot_api_aliases.toml` records three kinds of entry:
   - renames (`getMyCommands = "get_bot_commands"`);
   - not-applicable entries (`getUpdates`, `setWebhook`, `deleteWebhook`, `getWebhookInfo`,
     `close`, `logOut`);
   - "covered by a different shape" entries (`InputFile`, the `ChatMember*` family, which is one
     `ChatMember` with a status here).

   What remains is the real gap list, and the report diffs it against the previous Bot API version
   to show what each new release added.

A scheduled workflow (`.github/workflows/fork-coverage.yml`, weekly, plus `workflow_dispatch`)
runs both scripts and opens or updates one tracking issue on the fork with the reports. It runs
only on `Alb0204/kurigram` (`if: github.repository == 'Alb0204/kurigram'`). The report always goes
to the run's summary page; the issue (label `fork-report`) is only written while issues are
enabled on the fork.

Feature work driven by the coverage report goes into ordinary `feat/…` branches with
`Fork-only:` trailers. Pick by user value, not by count. The order that report points to today:
Bot API features that are only name gaps, which are cheap, then `messages`, `payments` and
`account` features that clients see, then `phone` (calls).

## 7. Conventions (from upstream's `CONTRIBUTING.md`)

- **Commits:** Conventional Commits with a scope, and identifiers in backticks
  (``fix(types): accept `None` in `User._parse()` ``). The subject says what changes and why.
- **No attribution** such as `Co-Authored-By` or `Claude-Session` trailers in commits, and no
  "Generated with Claude Code" line or other tool signature in PRs, issues or release notes. The
  only trailers allowed are `Upstream-PR:` and `Fork-only:`.
- **Generated code:** never hand-edit `pyrogram/raw/` or `pyrogram/errors/exceptions/`. Fix
  `compiler/` instead.
- **Gate before every push:** `make api && make lint && make typecheck && make test-unit`. Don't
  widen `ty` ignores or narrow `ruff` rules to get a change through.
- **Scope:** one concern per commit, like upstream, so a sync conflict touches one change and its
  ledger entry only.
- **Tests:** they go in `tests/unit/`, `tests/guards/` or `tests/integrations/` according to what
  they need. A test outside those three fails the run.

## 8. Using the fork from other projects

Depend on it by git URL with a tag rather than a branch, because the branch gets rebased. For
example, `kurigram @ git+https://github.com/Alb0204/kurigram@fork-v2.x.y-1`. Create a
`fork-vX.Y.Z-N` tag on `main` after each batch of adoptions, where `X.Y.Z` is upstream's version and
`N` counts fork releases on top of it. The `make tag` target pushes upstream-style `v*` tags, which
also trigger `pypi_release.yml`, so **never run `make tag` on the fork**. The fork has no PyPI
project.

## 9. Settled decisions (2026-10-28)

- Integration by rebase (§1).
- Mirrored upstream branches deleted from `origin` (§3).
- The `fast` extra depends on `tgcrypto-pyrofork>=1.2.9` from `Alb0204/tgcrypto-pyrofork`
  (`Fork-only: tgcrypto-pyrofork`). The original `tgcrypto` (1.2.5) has no wheels past cp311, and
  both distributions install the same `tgcrypto` module, so pulling in both makes one overwrite the
  other's files. 1.2.9 lives only on the fork's GitHub releases: `[tool.uv] find-links` covers
  uv, and pip users pass `--find-links https://github.com/Alb0204/tgcrypto-pyrofork/releases/expanded_assets/v1.2.9`.
  Bump that URL together with the floor on every tgcrypto-pyrofork release.
- Nothing is contributed upstream (the rule at the top of this file).
