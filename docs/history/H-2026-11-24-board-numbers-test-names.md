---
id: H-2026-11-24-board-numbers-test-names
title: Test names in the output of make board-numbers
status: closed
adrs: [R-77, R-86]
skills: [record, develop, review, python]
roadmap: []
proposals: []
---

# Test names in the output of make board-numbers

## Plan

The owner decided the planned row [R-86](../requirements/board-merge-report.md#r-86) with choice 1. `make board-numbers` prints the names of the tests of an id, not only their count.

## Develop

`board_numbers.py` has a new last column `names`. It lists each test that carries the id, as `file::name`. The column `tests` keeps the count. [R-86](../requirements/board-merge-report.md#r-86) is `in force`, and [R-77](../requirements/board-merge-report.md#r-77) names the column.

## Review

Gates passed in Podman after the last edit, including `make test` with 135 tests, `make lint`, `make format`, and `make links-check`. Security, privacy, interaction, and API checks were not touched. Not run: `make integration` and `make coverage`.

## Release

Not invoked: the owner merges and pushes this slice.
