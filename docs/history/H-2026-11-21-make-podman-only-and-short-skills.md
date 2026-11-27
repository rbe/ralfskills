---
id: H-2026-11-21-make-podman-only-and-short-skills
title: Make and Podman as the only interface, general rules, and short skills
status: closed
adrs: []
skills: [develop, review, record, project-setup, github-pipeline, release, python, shell]
decisions: [D-15, D-16, D-17]
proposals: []
issues: []
---

# Make and Podman as the only interface, general rules, and short skills

## Plan

`plan` was not invoked. The owner decided four things, recorded in D-15. Agents type only `make <target>` and Git commands.

## Develop

Every other tool runs in a Podman image behind a Make target. [R-75](../requirements/project-setup.md#r-75) states the interface, and [R-76](../requirements/project-setup.md#r-76) the shape of a skill. Rows changed because a sentence became false: [R-1](../requirements/record.md#r-1), [R-2](../requirements/project-setup.md#r-2), [R-3](../requirements/project-report.md#r-3), [R-5](../requirements/migrate-docs.md#r-5), [R-7](../requirements/plan.md#r-7), [R-8](../requirements/develop.md#r-8), [R-14](../requirements/plan.md#r-14), [R-16](../requirements/collection.md#r-16), [R-18](../requirements/collection.md#r-18), [R-19](../requirements/collection.md#r-19), [R-20](../requirements/record.md#r-20), [R-21](../requirements/project-setup.md#r-21), [R-28](../requirements/record.md#r-28), [R-34](../requirements/develop.md#r-34), [R-40](../requirements/project-setup.md#r-40), [R-43](../requirements/project-setup.md#r-43), [R-45](../requirements/project-setup.md#r-45), [R-46](../requirements/github-pipeline.md#r-46), [R-54](../requirements/develop.md#r-54), [R-57](../requirements/release.md#r-57), [R-60](../requirements/project-setup.md#r-60), [R-66](../requirements/collection.md#r-66), [R-72](../requirements/collection.md#r-72), and [R-73](../requirements/project-setup.md#r-73).

## Review

Reviewers found 38 findings, and 37 led to a change. Gates passed in Podman after the last edit. Not run: a real pull request merge, and macOS.

## Release

The orchestrator commits the branch. This slice does not merge it.
