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

`plan` was not invoked. The owner asked for item 4 of the trial review: a project needs a way to take a newer version of this collection, and a tag to pin.

Boundary: the README owns the update text. `onboard` only names it.

## Develop

The README has an `Update` section with five steps. It uses `apm update`, because APM 0.36.1 marks `apm install --update` as deprecated. [R-72](../REQUIREMENTS.md#r-72) states it. `onboard` step 10 names the pin when the collection has a tag.

The section warns that `apm update` overwrites a changed skill file, and that a new Makefile template does not change the `Makefile` of the project.

## Review

Gates through Make in Podman: see the Review of the slice that follows. The text was checked against `apm install --help` and `apm update --help` of APM 0.36.1.

security: a pinned `ref` stops a project from taking a changed default branch without a decision. No secret.

privacy, ux-ui-design, api-design: not touched.

No finding. Left alone: `apm update` itself was not run against a project in this slice. This collection has no tag yet. The owner creates the first tag after the merge.

## Release

Committed on the working branch with the next slice. The tag is the owner's step.
