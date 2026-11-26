---
id: H-2026-11-26-r-agents-section
title: Add the Agents section to the entry file
status: closed
adrs: [R-109, R-76]
skills: [r-record, r-project-setup]
roadmap: []
proposals: []
---

# Add the Agents section to the entry file

## Plan

The owner approved the text of the section. `r-plan` was not invoked.

## Develop

[R-109](../requirements/project-setup.md#r-109) is the rule. `CLAUDE.md` and its template have the section `## Agents`. The word limits of [R-76](../requirements/project-setup.md#r-76) rose by 94, the words of the section: 847 to 941 and 917 to 1011. No cut kept the meaning.

## Review

`make editorconfig`, `format`, `lint`, `test` (147 tests), and `coverage` (17 changed lines, 100%) passed. `make integration` is `true`. Each rule of the section has one owner: the section.

## Release

Not invoked: this slice does not ship.
