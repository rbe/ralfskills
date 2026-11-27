---
id: H-2026-11-26-component-upgrade-skills
title: The collection adds component-upgrade and one upgrade skill per language
status: closed
adrs: [R-104, R-76]
skills: [develop, review, record]
roadmap: []
proposals: []
---

# The collection adds component-upgrade and one upgrade skill per language

## Plan

On 2026-11-26 the owner chose one skill, `component-upgrade`, for all component updates, with one upgrade skill per language. `plan` was not invoked.

## Develop

[R-104](../requirements/component-upgrade.md#r-104) is the rule for the five skills. Each language skill lists the pins, the lock-file target, and the traps. The collection names no lock-file target for Python or Gradle, so those skills say so. [R-60](../requirements/project-setup.md#r-60) and the README name the five skills.

## Review

Gates passed after the last edit, including `make test` with 142 tests and `make coverage`, which reported 47 changed lines, all covered. The entry files stayed within the limits of [R-76](../requirements/project-setup.md#r-76), at 847 and 917 words. Security, privacy, and API checks were not touched.

## Release

Not invoked: the owner merges this slice.
