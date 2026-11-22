---
id: H-2026-11-20-gate-proof
title: Run every gate in its container and prove the selection with each runner
status: closed
adrs: [R-2]
skills: [develop, review, record, project-report, project-setup, github-pipeline, node, jvm, python, shell]
decisions: []
proposals: []
issues: []
---

# Run every gate in its container and prove the selection with each runner

## Plan

`plan` was not invoked. Three checks were open after the previous slice: the diff-cover step of `make coverage` in Podman, the Node coverage map with Jest and with Vitest, and the Gradle template in its JDK image.

Boundary: `project-setup` owns the diff-cover command in `tools.mk`. `node` names the selection for each test runner.

Pattern: a check that cannot run shows a defect in the recipe or a limit of the tool. The recipe changes, or the skill names the limit.

## Develop

diff-cover needs git. The recipe installed git with the package tool of the container on every run. `DIFF_COVER_IMAGE` is now an image that has git and Python, and the recipe installs no system package.

The Node coverage map is exact with `node --test` and with Jest, in ESM mode and in the default mode. The workers of Vitest write no V8 coverage, so the map is empty there. `vitest related --run` selects the right tests from the module graph. The `node` skill and the Makefile template name that command. D-8 records the choice.

The `gitignore` template lists `.gradle/`. Without it, the Gradle cache of the project was in the list of changed files.

Python and shell are the language skills.

## Review

Every gate passed through Make in Podman: `make test`, `make integration`, `make lint`, `make format`, `make editorconfig`, `make coverage`, `make test-changed`, `make ids`, `make toon`, `make project-report`, and `make decision-log`. The Python images came from `mirror.gcr.io`, because Docker Hub refused the pull. Podman on this machine uses the host network and the certificate bundle of the session.

The Gradle template ran in the image `eclipse-temurin:25-jdk` with Gradle 9.1.0 and JaCoCo 0.8.14, in a sample project. `make coverage` wrote the map and the diff report. After a change to one class, `make test-changed` ran the one test class that covers it, and the diff report named the changed line that no test ran.

Jest 29 and Vitest 3 ran in sample projects on this machine, not in a container.

security: no listener, no secret, no personal data in a fixture.

privacy: no personal data.

ux-ui-design: no screen.

api-design: not HTTP. Not a module export.

No finding. Left alone: the remote branch of the previous slices cannot be deleted from this machine.

## Release

The branch is pushed and merged into the default branch with a pull request, after the owner confirmed. This collection publishes no image.
