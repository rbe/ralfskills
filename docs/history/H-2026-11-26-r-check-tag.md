---
id: H-2026-11-26-r-check-tag
title: Add check-tag to stop a bad tag before the push
status: closed
adrs: [R-120, R-57]
skills: [r-record, r-github-pipeline]
roadmap: []
proposals: []
---

# Add check-tag to stop a bad tag before the push

## Plan

The owner asked for a target that fails before a tag push. `r-plan` was not invoked.

## Develop

[R-120](../requirements/github-pipeline.md#r-120) is the rule. `make check-tag TAG=vX.Y.Z` in `sdlc.mk` checks the format, that the tag is new and newer than every strict tag, and that `HEAD` is the tip of the default branch. No project has such a pattern. `finanzdesk/Makefile:307` has a `check-tag` that checks `package.json` and the lockfile, which is another rule. Tests run the real recipe in `sh` against a fake `git`.

## Review

`make editorconfig`, `format`, `lint`, `test` (176 tests), and `coverage` (100%) passed. `make integration` is `true`. The target did not run against a real repository.

## Release

Not invoked: this slice does not ship.
