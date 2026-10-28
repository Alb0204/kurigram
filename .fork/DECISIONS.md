# Fork decisions

One dated line per non-obvious call, newest first. Status alone lives in `ledger.json`.

- 2026-10-28: The fork only reads from upstream: no pushes, PRs, issues or comments there.
- 2026-10-28: Deleted the 27 mirrored upstream branches from `origin`; their head SHAs are in the ledger.
- 2026-10-28: Switched the `fast` extra to `tgcrypto-pyrofork>=1.2.9` (fork build with cp315 wheels).
- 2026-10-28: Confirmed: a linear stack on top of `upstream/main` (PLAN.md §1), because upstream squash-merges.
- 2026-10-28: Seeded the ledger. All 36 open upstream PRs and 13 open issues are `pending`.
