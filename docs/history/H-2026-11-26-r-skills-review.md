---
id: H-2026-11-26-r-skills-review
title: Add r-skills-review to find overlaps between skills
status: closed
adrs: [R-107, R-60, R-76]
skills: [r-record, r-skills-review, r-board-merge-report]
roadmap: []
proposals: []
---

# Add r-skills-review to find overlaps between skills

## Plan

The owner asked for a skill that finds and reports overlaps. `r-plan` was not invoked.

## Develop

[R-107](../requirements/skills-review.md#r-107) is the rule. The skill is in `skills/r-skills-review/`. `CLAUDE.md`, its template, [R-60](../requirements/project-setup.md#r-60), the README, the skill count test (30), and the purpose of `r-board-merge-report` changed. Word limits stay 847 and 917. Cuts: `(open work)` became `(open)` in `CLAUDE.md`, and `keep each only when installed` became `keep each installed one` in the template. The diagram is unchanged.

## Review

`make editorconfig`, `format`, `lint`, `test` (145 tests), and `coverage` (100%) passed. `make integration` is `true`.

## Release

Not invoked: this slice does not ship.
