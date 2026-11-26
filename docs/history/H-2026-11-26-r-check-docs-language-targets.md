---
id: H-2026-11-26-r-check-docs-language-targets
title: Stop check-docs failing where r-jvm is not installed
status: closed
adrs: [R-111, R-122]
skills: [r-github-pipeline, r-project-setup]
roadmap: []
proposals: []
---

# Stop check-docs failing where r-jvm is not installed

## Plan

The update of the product repositories to v0.6.0 found the defect. `r-plan` was not invoked.

## Develop

`references/setup-files.md` of `r-github-pipeline` named `make wrapper`, `make jvm-tooling`, `make podman-socket`, `make npm`, and `make node-tooling`. In dashboard, ernaehrung, and reelbox, `r-jvm` is not installed, so `make check-docs` failed and `make test` failed with it. The text now names these as targets without `make`. A unit test of [R-111](../requirements/project-setup.md#r-111) fails when a skill other than the language skill or its upgrade skill names `make <target>` for a target of a language file of [R-122](../requirements/collection.md#r-122).

## Review

The new test failed before the text change and passes after it. `make test`, `lint`, `format`, and `editorconfig` ran; see the pull request.

## Release

Not invoked: this slice does not ship.
