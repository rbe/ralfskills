---
id: H-2026-11-26-accessibility-observability-performance
title: The collection adopts accessibility, observability, and performance checks
status: closed
adrs: [R-33, R-102, R-103, R-76]
skills: [develop, review, record]
roadmap: []
proposals: []
---

# The collection adopts accessibility, observability, and performance checks

## Plan

On 2026-11-26 the owner chose to extend `ux-ui-design` with accessibility checks and to add `observability` and `performance`. The source is the OrgMe skills of `rbe/finanzdesk`, written without product detail. `plan` was not invoked.

## Develop

`ux-ui-design` has two more questions and nine checks. [R-33](../requirements/ux-ui-design.md#r-33) holds the new text. [R-102](../requirements/observability.md#r-102) is the rule for `observability`, and [R-103](../requirements/performance.md#r-103) the rule for `performance`. The baseline rule moved there from [R-48](../requirements/review.md#r-48). [R-30](../requirements/plan.md#r-30) and the entry files name the two new skills.

## Review

Gates passed after the last edit, including `make test` with 141 tests and `make coverage`, which reported 38 changed lines, all covered. The skill count is now 24. The entry-file word limits rose to 847 and 917, as [R-76](../requirements/project-setup.md#r-76) states. Security, privacy, and API checks were not touched.

## Release

Not invoked: the owner merges the pull request.
