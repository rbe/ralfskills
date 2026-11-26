---
id: H-2026-11-26-r-review-rules
title: Adopt the review rules of emailtodisk
status: closed
adrs: [R-113, R-114, R-108, R-48]
skills: [r-record, r-review, r-release]
roadmap: []
proposals: []
---

# Adopt the review rules of emailtodisk

## Plan

The owner approved three rules from `emailtodisk`. `r-plan` was not invoked.

## Develop

[R-113](../requirements/record.md#r-113) is the defect report form, in `r-record`. `r-review` points to it, and [R-48](../requirements/review.md#r-48) no longer lists the parts. [R-114](../requirements/release.md#r-114) is the staging rule, in `r-release`. The re-check of an agent claim is in the Agents section already, so it is not repeated. [R-108](../requirements/collection.md#r-108) names the hook for the plugin. The hook is not added.

## Review

`make editorconfig`, `format`, `lint`, `test` (167 tests), and `coverage` (100%) passed. `make integration` is `true`. The finding sentence of `r-review` moved to `r-record`, so the parts have one owner.

## Release

Not invoked: this slice does not ship.
