---
id: H-2026-11-18-plan-costly-choice
title: Plan waits on a costly choice
status: closed
adrs: [ADR-0014, ADR-0007]
skills: [plan, develop, record, python]
decisions: []
proposals: []
issues: []
---

# Plan waits on a costly choice

## Plan

The owner named the step and its wording. When a choice is expensive to reverse, the step names the options, recommends one, and waits. Otherwise the slice continues in small modules. `plan` owns the architect step.

## Develop

The step is number 5 in `skills/plan/SKILL.md`, after the boundary step. ADR-0014 quotes that paragraph. The collection test proves that the paragraph is that numbered step. Python is the language skill for the test.

## Review

`make editorconfig`, `make format`, `make lint`, `make test`, `make integration`, `make coverage`, and `make project-report` passed. `make ids` passed through `make py`. No finding. Security, privacy, interaction, and API checks found nothing.

## Release

Not invoked: this slice does not ship.
