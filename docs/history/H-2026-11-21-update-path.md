---
id: H-2026-11-21-update-path
title: The update path and version tags are documented
status: closed
adrs: []
skills: [develop, review, record, onboard]
decisions: []
proposals: []
issues: []
---

# The update path and version tags are documented

## Plan

`plan` was not invoked. The owner asked for a way to take a newer version of this collection, and a tag to pin. The README owns the update text.

## Develop

The README has an `Update` section with five steps. It uses `apm update`, because APM 0.36.1 marks `apm install --update` as deprecated. [R-72](../requirements/collection.md#r-72) states it.

## Review

The text was checked against the help output of APM 0.36.1. A pinned `ref` stops a project from taking a changed default branch without a decision. No finding.

## Release

Committed on the working branch. The owner creates the first tag after the merge.
