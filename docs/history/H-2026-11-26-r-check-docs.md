---
id: H-2026-11-26-r-check-docs
title: Add the check-docs target
status: closed
adrs: [R-111, R-105]
skills: [r-record, r-project-setup, r-project-report]
roadmap: []
proposals: []
---

# Add the check-docs target

## Plan

The owner approved the drift check of `finanzdesk`. `r-plan` was not invoked.

## Develop

[R-111](../requirements/project-setup.md#r-111) is the rule. `check-docs.mk` and `check_docs.py` are in `r-project-setup`, and `make test` runs the target. The check found one drift: the commit that added the `r-` prefix renamed the target `project-report` to `r-project-report` in `report.mk` and `contract.mk`, against [R-105](../requirements/collection.md#r-105). Both files, `project.mk`, the docs of the target, and one test name `project-report` again. The check found no wrong path.

## Review

`make editorconfig`, `format`, `lint`, `test` (164 tests, and `check-docs`), and `coverage` (264 changed lines against main, 100%) passed. `make integration` is `true`. The check states no rule that another skill states.

## Release

Not invoked: this slice does not ship.
