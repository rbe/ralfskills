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

The owner named the step and the wording. `plan` already names who owns state and what may call what. The new step follows that one.

Boundary: `plan` owns the architect step. The paragraph stays the words the owner gave.

Pattern: the step is a numbered line under Work. When a choice is expensive to reverse, the step names the options, recommends one, and waits. Otherwise the slice continues in small modules.

## Develop

The step is number 5 in `skills/plan/SKILL.md`, immediately after the boundary step. ADR-0014 quotes that paragraph. The collection test proves the paragraph is that next numbered step. Python is the language skill for the test.

## Review

`make` with no target prints help. `make editorconfig`, `make format`, `make lint`, `make test`, `make integration`, `make coverage`, and `make project-report` passed. `make ids` passed through `make py`.

security: no listener, no secret, no personal data in a fixture.

privacy: no personal data.

ux-ui-design: no screen.

api-design: no HTTP route. The step is skill text. The test stays internal.

No finding. Left alone: the other skills, the Makefile, and the default goal `help`.

## Release

Not invoked: this slice does not ship.
