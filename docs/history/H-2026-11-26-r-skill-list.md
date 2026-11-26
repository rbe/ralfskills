---
id: H-2026-11-26-r-skill-list
title: Keep one list of the skills
status: closed
adrs: [R-16, R-60]
skills: [r-record, r-project-setup]
roadmap: []
proposals: []
---

# Keep one list of the skills

## Plan

The owner asked for one owner of the skill list. `r-plan` was not invoked.

## Develop

[R-16](../requirements/collection.md#r-16) listed 22 skills, and the collection has 30 folders in `skills/`. [R-60](../requirements/project-setup.md#r-60) named only some of them, so it could not be the owner as it stood. [R-60](../requirements/project-setup.md#r-60) now has the full list of 30 names, and [R-16](../requirements/collection.md#r-16) points to [R-60](../requirements/project-setup.md#r-60). A test compares the [R-60](../requirements/project-setup.md#r-60) list with the folders of `skills/` and checks that [R-16](../requirements/collection.md#r-16) names no skill.

## Review

`make editorconfig`, `format`, `lint`, `test` (177 tests), and `coverage` (100%) passed. `make integration` is `true`.

## Release

Not invoked: this slice does not ship.
