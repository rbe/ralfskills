---
id: H-2026-11-16-requirement-tests
title: Tests name requirements
status: closed
adrs: [ADR-0001, ADR-0002, ADR-0003]
skills: [develop, review, project-setup, project-report, record, python, shell]
decisions: []
proposals: []
issues: []
---

# Tests name requirements

## Plan

The owner accepted three rules. A test names the requirement it proves in an `id:` line. `make test` stays the full suite. `make project-report` is the only writer of `build/project-report.md`.

## Develop

`project-report` generates the report. The skills `develop`, `review`, `project-setup`, and `record` carry the rules as numbered steps. Python is the language skill for the report, the coverage map, and the selector. Shell is the language skill for the Make recipes.

## Review

`make editorconfig`, `make format`, `make lint`, `make test`, `make integration`, `make coverage`, `make project-report`, and `make test-changed` passed. No finding. Security, privacy, interaction, and API checks found nothing.

## Release

Not invoked: this slice does not ship.
