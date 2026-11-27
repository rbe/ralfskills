---
id: H-2026-11-25-cover-ten-rows
title: Cover ten requirement rows that tests pin
status: closed
adrs: [R-1, R-2, R-3, R-6, R-13, R-28, R-69, R-76, R-77, R-84]
skills: [board-merge, board-merge-report, record, review]
roadmap: []
proposals: []
---

# Cover ten requirement rows that tests pin

## Plan

The owner merged PR 28 and asked to apply the `cover` action of `board-merge` to ten rows: [R-13](../requirements/record.md#r-13), [R-6](../requirements/record.md#r-6), [R-84](../requirements/record.md#r-84), [R-76](../requirements/project-setup.md#r-76), [R-69](../requirements/record.md#r-69), [R-3](../requirements/project-report.md#r-3), [R-2](../requirements/project-setup.md#r-2), [R-1](../requirements/record.md#r-1), [R-77](../requirements/board-merge-report.md#r-77), and [R-28](../requirements/record.md#r-28).

## Develop

Two agents made nine commits, one for each changed row, and only `docs/requirements/` changed. [R-13](../requirements/record.md#r-13) has no commit, because only one of its sentences is pinned by a test. The rows hold 2512 words after the cover. Each deleted sentence has a pinning test, so no fact was restored.

## Review

Gates passed in Podman after the last edit, including `make toon`, `make links`, `make ids`, `make links-check`, `make format`, `make lint`, and `make test` with 135 tests. Security, privacy, interaction, and API checks were not touched. Not run: `make integration` and `make coverage`.

## Release

Not invoked: the owner pushes this slice.
