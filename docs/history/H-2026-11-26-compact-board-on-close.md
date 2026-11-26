---
id: H-2026-11-26-compact-board-on-close
title: Record compacts the board when it closes a task
status: closed
adrs: [R-106, R-58]
skills: [r-record, r-board-merge, r-board-merge-report]
roadmap: []
proposals: []
---

# Record compacts the board when it closes a task

## Plan

The owner decided that a close shortens the history file and deletes the proposal. `r-plan` was not invoked.

## Develop

[R-106](../requirements/record.md#r-106) is the rule. `close.md`, `id-kinds.md`, [R-58](../requirements/record.md#r-58), and the README changed. `r-board-merge` and `r-board-merge-report` had no contradicting sentence. Old history files are unchanged.

## Review

`make editorconfig`, `format`, `lint`, `test` (144 tests), and `coverage` (100%, 108 lines) passed. `make integration` is `true`.

## Release

Not invoked: this slice does not ship.
