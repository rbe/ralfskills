---
id: H-2026-11-26-r-board-only-push
title: Skip setup, build, and test for a push of board files only
status: closed
adrs: [R-123, R-93, R-57]
skills: [r-record, r-github-pipeline]
roadmap: []
proposals: []
---

# Skip setup, build, and test for a push of board files only

## Plan

The owner asked that the close of a task, which is its own merge, runs no pipeline, because the branch of the task already ran it. `r-plan` was not invoked. The owner keeps the separate close.

## Develop

[R-123](../requirements/github-pipeline.md#r-123) is the rule. `make ci-scope` in `sdlc.mk` compares `HEAD` with `github.event.before`, or with the merge base of the default branch. If every changed file is in `CI_BOARD_FILES` and `make ci-status` passes for that base, it writes `board-only=true`. The three workflow templates skip `make setup`, `build`, and `test` on that output. `report` still runs. Tests run the real recipe in `sh` against a fake `git` and a fake `ci-status`.

## Review

`make editorconfig`, `format`, `lint`, `test` (200 tests), and `coverage` passed. `make integration` is `true`. The workflow did not run on GitHub.

## Release

Not invoked: this slice does not ship.
