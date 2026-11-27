---
id: H-2026-11-20-gate-proof
title: Run every gate in its container and prove the selection with each runner
status: closed
adrs: []
skills: [develop, review, record, project-report, project-setup, github-pipeline, node, jvm, python, shell]
decisions: [D-8]
proposals: []
issues: []
---

# Run every gate in its container and prove the selection with each runner

## Plan

`plan` was not invoked. Three checks were open: diff-cover in Podman, Node coverage with Jest and Vitest, and the Gradle template in its JDK image.

## Develop

diff-cover needs git, so `DIFF_COVER_IMAGE` now has git and Python. The Node coverage map is exact with `node --test` and Jest. Vitest selects tests with `vitest related --run`, and D-8 records that choice. Python and shell are the language skills.

## Review

Gates passed in Podman, including `make test`, `make lint`, `make format`, `make coverage`, and `make test-changed`. The Gradle template ran in `eclipse-temurin:25-jdk`. Jest and Vitest ran on the host, not in a container. No finding.

## Release

The branch is pushed and merged into the default branch with a pull request, after the owner confirmed. This collection publishes no image.
