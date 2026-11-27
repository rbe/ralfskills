---
id: H-2026-11-25-readme-migration-facts
title: The README states three facts for the migration of a project
status: closed
adrs: [R-72]
skills: [develop, review, record]
roadmap: []
proposals: []
---

# The README states three facts for the migration of a project

## Plan

The owner migrates existing projects onto the collection and asked for three facts in the README. `plan` was not invoked. The repository holds no diagram, so no diagram changed.

## Develop

The README states three facts: `make old-board` fails first with the only skill `migrate-docs`, `make apm ARGS='install --force'` overwrites unmanaged skill files, and `make id-raise KIND=<kind> TO=<n>` raises a counter. [R-72](../requirements/collection.md#r-72) has one sentence that states them. One test pins the three facts.

## Review

Gates passed after the last edit, including `make toon`, `make links`, `make ids`, `make test` with 137 tests, and `make lint`. Security, privacy, interaction, and API checks were not touched. Not run: `make integration` and `make coverage`.

## Release

Not invoked: the owner pushes this slice.
