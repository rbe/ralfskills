---
id: H-2026-11-20-round-five
title: Fix what a fifth trial round found
status: closed
adrs: []
skills: [plan, develop, review, release, record, project-setup, migrate-docs, go, python, security, shell]
decisions: []
proposals: []
issues: []
---

# Fix what a fifth trial round found

## Plan

`plan` was not invoked. Two new agents ran a trial round from the default branch. One set up a Go project, and one onboarded a Python project and delivered a feature.

## Develop

The Go template built with an output directory, which failed for a library. It now compiles every package. A pipe hid a missing coverage map. `make coverage` removes the earlier report first. Shell is the language skill.

## Review

Gates passed in Podman with the pinned images. On a copy of the Go trial project, `make test-changed` selected the package of the changed file. No finding. The cause of one Podman error is not known.

## Release

The branch is pushed. This slice does not merge it.
