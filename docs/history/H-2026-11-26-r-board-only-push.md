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

The owner asked that the close of a task runs no pipeline, because the task's branch already ran it. `r-plan` was not invoked. The owner keeps the separate close.

## Develop

[R-123](../requirements/github-pipeline.md#r-123) is the rule. `make ci-scope` compares `HEAD` with the previous push. If every changed file is a board file and `make ci-status` passes, it writes `board-only=true`. The three workflow templates skip `setup`, `build`, and `test` on that output.

## Review

Gates passed after the last edit: `make editorconfig`, `make format`, `make lint`, `make test` (200 tests), and `make coverage`. `make integration` is `true`. The workflow did not run on GitHub.

## Release

Not invoked: this slice does not ship.
