---
id: H-2026-11-20-adr-rules
title: Require the ADR rules and remove the wording tests
status: closed
adrs: []
skills: [plan, develop, review, record, project-report, python]
decisions: [D-5]
proposals: []
issues: []
---

# Require the ADR rules and remove the wording tests

## Plan

`plan` was not invoked. The owner named four rows and the removal. [R-53](../requirements/record.md#r-53) to [R-56](../requirements/record.md#r-56) state the ADR rules. `record` owns the status rule.

## Develop

[R-53](../requirements/record.md#r-53) to [R-56](../requirements/record.md#r-56) are rows of `docs/REQUIREMENTS.md`. [R-54](../requirements/develop.md#r-54) and [R-55](../requirements/record.md#r-55) sit in the steps that read them. Two wording test files were deleted. The project report lists [R-4](../requirements/record.md#r-4), [R-5](../requirements/migrate-docs.md#r-5), [R-7](../requirements/plan.md#r-7), [R-12](../requirements/project-setup.md#r-12), [R-14](../requirements/plan.md#r-14), and [R-16](../requirements/collection.md#r-16) to [R-52](../requirements/collection.md#r-52) as ids with no test.

## Review

`make lint` and `make test` did not run, because this machine has no Podman. The script tests and the id check passed under host `python3`. Security, privacy, interaction, and API checks found nothing.

## Release

Not invoked: this slice does not ship.
