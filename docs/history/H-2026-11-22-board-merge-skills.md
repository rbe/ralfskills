---
id: H-2026-11-22-board-merge-skills
title: The skills board-merge-report and board-merge
status: closed
adrs: [R-77, R-78]
skills: [develop, review, record, project-setup, board-merge-report, board-merge, python, shell]
decisions: [D-18]
proposals: []
issues: []
---

# The skills board-merge-report and board-merge

## Plan

`plan` was not invoked. The owner set the scope, the four finding kinds, and the split into two skills. `board-merge-report` writes nothing. `board-merge` writes only through `record`.

## Develop

`board_numbers.py` prints the numbers of each unit, behind `make board-numbers`. [R-16](../requirements/collection.md#r-16) names both skills. Rows [R-77](../requirements/board-merge-report.md#r-77) and [R-78](../requirements/board-merge.md#r-78) and D-18 state the choice.

## Review

A trial on a repository copy applied three findings, one commit each. Restored: [R-30](../requirements/plan.md#r-30), [R-46](../requirements/github-pipeline.md#r-46), [R-57](../requirements/release.md#r-57), and [R-60](../requirements/project-setup.md#r-60). Corrected: [R-1](../requirements/record.md#r-1), [R-3](../requirements/project-report.md#r-3), [R-11](../requirements/project-setup.md#r-11), [R-20](../requirements/record.md#r-20), [R-25](../requirements/plan.md#r-25), [R-27](../requirements/record.md#r-27), [R-29](../requirements/migrate-docs.md#r-29), [R-42](../requirements/github-pipeline.md#r-42), [R-44](../requirements/project-setup.md#r-44), [R-45](../requirements/project-setup.md#r-45), [R-63](../requirements/project-report.md#r-63), and [R-73](../requirements/project-setup.md#r-73). Framework detail moved: [R-36](../requirements/node.md#r-36), [R-37](../requirements/python.md#r-37), and [R-39](../requirements/jvm.md#r-39). Duplicates removed: [R-13](../requirements/record.md#r-13), [R-24](../requirements/record.md#r-24), [R-28](../requirements/record.md#r-28), [R-40](../requirements/project-setup.md#r-40), [R-48](../requirements/review.md#r-48), [R-71](../requirements/project-setup.md#r-71), and [R-75](../requirements/project-setup.md#r-75). Open rows D-19 to D-24 hold the open work.

## Release

Not invoked: the owner merges this slice.
