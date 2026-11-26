---
id: H-2026-11-26-r-agent-agnostic-text
title: Say that R-17 is about AI coding tools and models
status: closed
adrs: [R-17]
skills: [r-record]
roadmap: []
proposals: []
---

# Say that R-17 is about AI coding tools and models

## Plan

The owner gave the new statement. `r-plan` was not invoked.

## Develop

[R-17](../requirements/collection.md#r-17) now names AI coding tools, tool folders, and models, and says that `grep` and `podman` are not AI coding tools. A unit test scans each `SKILL.md` and each reference file for `Cursor`, `.agents/`, `.cursor/`, `Fable`, `Opus`, `Sonnet`, and `Haiku`. It found no hit, so no skill text changed. No new id.

## Review

`make editorconfig`, `format`, `lint`, `test` (148 tests), and `coverage` (100%) passed. `make integration` is `true`. The Agents section and [R-17](../requirements/collection.md#r-17) do not state the same rule: [R-17](../requirements/collection.md#r-17) bans names in skill text, and the section is the one place that names models.

## Release

Not invoked: this slice does not ship.
