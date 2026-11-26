---
id: H-2026-11-26-r-stage-routing
title: Add the stages column to the skill index
status: closed
adrs: [R-110, R-6, R-30, R-34, R-49]
skills: [r-record, r-plan, r-develop, r-review]
roadmap: []
proposals: []
---

# Add the stages column to the skill index

## Plan

The owner approved the idea of `finanzdesk`: one table says which stage loads which skill. `r-plan` was not invoked.

## Develop

[R-110](../requirements/record.md#r-110) is the rule. Each check skill has `stages: [r-plan, r-review]` and each language skill has `stages: [r-develop]`. `skill_index.py` writes the column. `r-plan`, `r-develop`, and `r-review` read it. [R-34](../requirements/develop.md#r-34), [R-49](../requirements/plan.md#r-49), and [R-6](../requirements/record.md#r-6) name it. `r-project-report` has no `kind`, so it has no row.

## Review

`make editorconfig`, `format`, `lint`, `test` (150 tests), and `coverage` (100%) passed. `make integration` is `true`. [R-30](../requirements/plan.md#r-30) still says who runs each subskill. I kept it, because it states the behaviour and not the column.

## Release

Not invoked: this slice does not ship.
