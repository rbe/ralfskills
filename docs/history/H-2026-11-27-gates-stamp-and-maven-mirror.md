---
id: H-2026-11-27-gates-stamp-and-maven-mirror
title: Gates once with a stamp, quiet undefined variables, and a Maven mirror
status: open
adrs: [R-8, R-57, R-71, R-127, R-128]
skills: [plan, develop, review, record]
roadmap: []
proposals: []
---

# Gates once with a stamp, quiet undefined variables, and a Maven mirror

## Plan

The owner chose a stamp file and a git pre-push hook. The six gates run once, in `r-review`. `r-develop` runs only `make test-changed` and `make coverage`. The owner approved `MAVEN_MIRROR` for HTTP 429 from Maven Central. The owner reported undefined-variable warnings from `make setup` and `make build` in finanzdesk.

## Develop

`THIS_MAKE` moved to `tools.mk`, before `contract.mk` reads it. Each command variable has an empty default. `make gates` writes `build/gates.ok` ([R-127](../requirements/project-setup.md#r-127)). `make gates-check` and the pre-push hook compare it. `jvm.mk` mounts `maven-mirror.gradle` when `MAVEN_MIRROR` is set ([R-128](../requirements/jvm.md#r-128)). A Sonnet agent wrote the stamp and the hook. The orchestrator wrote the rest and reviewed the agent.

## Review

`make gates` passed: editorconfig, format, lint, test (256 tests), integration, and coverage. `make gates-check`, `links-check`, `check-docs`, and `ids` passed. In erechnung, `make setup` with `MAVEN_MIRROR` fetched 351 files from the mirror. In finanzdesk, `make --warn-undefined-variables -n` printed no warning.

## Release

