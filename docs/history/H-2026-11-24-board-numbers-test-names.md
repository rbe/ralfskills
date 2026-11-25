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

The owner decided the planned row [R-86](../requirements/board-merge-report.md#r-86) with choice 1: `make board-numbers` prints the names of the tests of an id, and not only their count.

## Develop

`skills/board-merge-report/scripts/board_numbers.py` has a new last column `names`. It holds each test that carries the id in a line `id:`, written as `file::name`, sorted, and joined with `;`. The column `tests` keeps the count. The output stays one line for each unit. A test file with no readable declaration is named by its file alone, and a unit with no test has an empty cell. The function `test_counts` is replaced by `test_names`, and `declared_name` finds the declaration of one test. It reads Python, Go, Java, Kotlin, Groovy, and JavaScript declarations.

`skills/board-merge-report/scripts/test_board_numbers.py` has two new tests with `id: R-86`. The test of the output form changed to the new header and the sample line of the first sample requirement row. The help text and the header comment of `skills/board-merge-report/merge-report.mk`, `SKILL.md` and `references/finding-kinds.md` and `references/report-form.md` of `board-merge-report`, and `SKILL.md` of `board-merge` name the column `names`. [R-86](../requirements/board-merge-report.md#r-86) is `in force`, and [R-77](../requirements/board-merge-report.md#r-77) names the column.

## Review

The gates ran through Make in Podman after the last edit. `make lint` passed. `make test` passed with 135 tests. `make editorconfig` and `make format` passed. `make toon`, `make links`, `make ids`, and `make links-check` passed.

security, privacy, ux-ui-design, api-design: not touched.

Not run: `make integration` and `make coverage`.

## Release

Not invoked: the owner merges and pushes this slice.
