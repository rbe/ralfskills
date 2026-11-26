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

On 2026-11-26 the owner chose to extend `ux-ui-design` with accessibility checks, and to add the subskills `observability` and `performance`. The source is the OrgMe skills `accessibility`, `observability`, and `performance` of `rbe/finanzdesk`. The three topics are written without any product detail. `plan` was not invoked.

## Develop

`skills/ux-ui-design/SKILL.md` has two more questions and nine checks. The old contrast check now names WCAG 2.2 level AA, so contrast is stated once. [R-33](../requirements/ux-ui-design.md#r-33) holds the new text.

[R-102](../requirements/observability.md#r-102) is the new rule for `skills/observability/SKILL.md`, order 50. It points to `privacy` for personal data in logs and to `api-design` for the error body.

[R-103](../requirements/performance.md#r-103) is the new rule for `skills/performance/SKILL.md`, order 60. The baseline rule moved there from `skills/review/SKILL.md` and from [R-48](../requirements/review.md#r-48), so one skill states it.

The subskill lists in `CLAUDE.md`, in the `CLAUDE.md` template of `project-setup`, in [R-30](../requirements/plan.md#r-30), and in the skill table of the README name the two new skills. The `apm.yml` sample of the README lists no subskill, so it did not change.

Tests in `skills/project-report/scripts/test_project_report.py` name `id: R-33`, `id: R-102`, and `id: R-103`.

## Review

After the last edit, `make toon`, `make links`, `make ids`, `make links-check`, `make format-fix`, `make editorconfig`, `make format`, `make lint`, `make test`, `make integration`, and `make coverage` passed. `make test` ran 141 tests. `make coverage` reports 38 changed lines, all covered. The gates ran in a cloud container with Docker behind a `podman` shim.

Two tests needed an update because the change adds two skills and two subskill names. The skill count is now 24. The word limits of `CLAUDE.md` and its template rose by 2, to 847 and 917, one word for each new name. [R-76](../requirements/project-setup.md#r-76) states the new limits.

security, privacy, api-design: not touched. ux-ui-design: changed. observability, performance: new.

## Release

Not invoked: the owner merges the pull request.
