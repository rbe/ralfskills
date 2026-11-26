---
id: H-2026-11-26-r-gradle-podman
title: Let Gradle in Podman reach Podman
status: closed
adrs: [R-116]
skills: [r-record, r-jvm, r-github-pipeline]
roadmap: []
proposals: []
---

# Let Gradle in Podman reach Podman

## Plan

The owner decided: Gradle runs in a container and reaches Podman, so the host needs no Java toolchain. `r-plan` was not invoked.

## Develop

[R-116](../requirements/jvm.md#r-116) is the rule, and `r-jvm` owns it. Both `templates/Makefile.gradle` files have `PODMAN_SOCKET`, `GRADLE_PODMAN`, and `podman-socket`. The pattern comes from `odisee26/Makefile:102-120` and `:152-166`, and `odisee26/docs/pipeline-rules.md:42`. The template has no `systemctl` branch.

## Review

`make editorconfig`, `format`, `lint`, `test` (169 tests), and `coverage` (100%) passed. `make integration` is `true`. No template ran against a real Gradle project.

## Release

Not invoked: this slice does not ship.
