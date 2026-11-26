---
id: H-2026-11-26-r-stage-addenda
title: Allow stage addenda of a project
status: closed
adrs: [R-112, R-76]
skills: [r-record, r-project-setup]
roadmap: []
proposals: []
---

# Allow stage addenda of a project

## Plan

The owner approved the rule, after `finanzdesk` with `orgme-plan`. `r-plan` was not invoked.

## Develop

[R-112](../requirements/project-setup.md#r-112) is the rule. It stands once in `CLAUDE.md` and its template, beside the sentence that defines a project skill, so no stage skill repeats it. The word limits of [R-76](../requirements/project-setup.md#r-76) rose by 25, the words of the rule: 941 to 966 and 1011 to 1036.

## Review

`make editorconfig`, `format`, `lint`, `test` (165 tests), and `coverage` (100%) passed. `make integration` is `true`. The rule has one owner, the entry file.

## Release

Not invoked: this slice does not ship.
