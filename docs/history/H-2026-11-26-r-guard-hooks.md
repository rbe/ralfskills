---
id: H-2026-11-26-r-guard-hooks
title: Ship the guard hooks of emailtodisk
status: closed
adrs: [R-124, R-108, R-114]
skills: [r-record]
roadmap: []
proposals: []
---

# Ship the guard hooks of emailtodisk

## Plan

The owner asked to move the two guard hooks of `rbe/emailtodisk` into this collection. `r-plan` was not invoked. [R-108](../requirements/collection.md#r-108) planned the hooks in a plugin. APM 0.36.1 installs a `hooks/*.json` file of a package into `.claude/settings.json`, so the hooks need no plugin.

## Develop

[R-124](../requirements/collection.md#r-124) states the hooks. `hooks/r-guards.json` names `block-bare-git-add.sh` and `block-python-file-write.sh` in `hooks/scripts/`. `hook-command.sh` reads the command from the hook input with POSIX `awk`, so the scripts need no `jq`. In emailtodisk a missing `jq` let every command pass. Now a hook input without a command exits 2 and blocks the command. The git hook also refuses `git commit -a`, `git add :/`, and `git -C <dir> add .`, because [R-114](../requirements/release.md#r-114) names them or they stage the whole working copy. The Python hook refuses a write to any quoted relative path outside `build/`, not only `src/` and `docs/`, and it also matches `make py`. [R-108](../requirements/collection.md#r-108) no longer names the hooks. `.claude/settings.json` of this collection runs the scripts here. `tests/test_hooks.py` runs each script with sample hook input. The README has the section "Guard hooks".

`apm install` of the pushed branch ran in a sample project that names only `r-record` and `r-shell`. It copied `hooks/` to `.claude/hooks/ralfskills/hooks/`, added both hooks to `.claude/settings.json`, and kept the other settings. The installed git hook refused `git add .`. The tests passed with mawk and with the original awk (one-true-awk, the base of the macOS awk).

## Review

`make editorconfig`, `format`, `lint`, `test` (208 tests, 8 of them new), `ids`, `links-check`, and `check-docs` passed. `make integration` is `true`. `make coverage` passed and found no measured line in the diff, because the coverage tool measures Python and the new code is shell. The tests ran the shell scripts with mawk and with the original awk (one-true-awk, the base of the macOS awk). A run on macOS was not done. emailtodisk was not changed: it keeps its own copies until it takes the next version.

## Release

Not invoked: this slice does not ship.
