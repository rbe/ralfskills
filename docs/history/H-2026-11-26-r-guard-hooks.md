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

The owner asked to move the two guard hooks of `rbe/emailtodisk` into this collection. `r-plan` was not invoked. [R-108](../requirements/collection.md#r-108) had planned the hooks in a plugin. APM installs the hooks file into `.claude/settings.json`, so no plugin is needed.

## Develop

[R-124](../requirements/collection.md#r-124) states the hooks. A hook input without a command now exits 2 and blocks. The git hook also refuses `git commit -a`, `git add :/`, and `git -C <dir> add .`, as [R-114](../requirements/release.md#r-114) requires. `tests/test_hooks.py` runs each script with sample input.

## Review

Gates passed: `make editorconfig`, `make format`, `make lint`, `make test` (208 tests), `make ids`, `make links-check`, and `make check-docs`. `make integration` is `true`. The scripts passed with mawk and the original awk. A macOS run was not done.

## Release

Not invoked: this slice does not ship.
