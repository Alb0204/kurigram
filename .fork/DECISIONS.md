# Fork decisions

One dated line per non-obvious call, newest first. Status alone lives in `ledger.json`.

- 2026-10-29: Kept the 3.10 floor until upstream drops it, although 3.10 reached end-of-life on 2026-10-01 (devguide.python.org/versions): moving it here alone would make the fork harder to rebase. Pinned `[tool.ty.environment] python-version = "3.14"` so the editor stops greying `import tomllib` in `.fork/scripts/coverage.py`; ty otherwise resolved 3.10 from `requires-python`. The pin also hides 3.10-only breakage from ty, so drop it when the floor moves.
- 2026-10-29: Finished the first pass over all 36 open upstream pull requests: 28 adopted, 8 deferred (#521, #523, #488, #527, #471, #450, #479, #559), none rejected. Each deferral has its reason in `ledger.json`.
- 2026-10-29: Deferred #521 rather than resolve its 10 conflicts here: a 162-file, unreviewed refactor carried in a fork-specific form would collide with whatever upstream finally merges.
- 2026-10-29: Adopted #548 although it removes `GiftAttribute.date`, `caption`, `caption_entities`, `from_user` and `to_user`: only an unreachable, broken branch ever set them, and none of the user's projects read them.
- 2026-10-29: Coverage baseline: layer 232 (0 behind), 490 of 819 tracked raw functions unwrapped, 141 Bot API 10.3 names with no counterpart (34 methods, 107 types). Type parity is by name and kurigram names types after TDLib, so most type gaps are naming, not missing features; only verified mappings are aliased.
- 2026-10-28: The fork only reads from upstream: no pushes, PRs, issues or comments there.
- 2026-10-28: Deleted the 26 mirrored upstream branches from `origin`; their head SHAs are in the ledger.
- 2026-10-28: Switched the `fast` extra to `tgcrypto-pyrofork>=1.2.9` (fork build with cp315 wheels), found through `[tool.uv] find-links` on the fork's v1.2.9 GitHub release because it is not on PyPI.
- 2026-10-28: Confirmed: a linear stack on top of `upstream/main` (PLAN.md §1), because upstream squash-merges.
- 2026-10-28: Seeded the ledger. All 36 open upstream PRs and 13 open issues are `pending`.
