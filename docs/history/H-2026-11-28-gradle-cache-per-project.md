---
id: H-2026-11-28-gradle-cache-per-project
title: Each project has its own Gradle cache
status: closed
adrs: [R-154, R-159]
skills: [r-record, r-develop, r-review]
roadmap: []
proposals: []
---

# Each project has its own Gradle cache

## Plan

`r-plan` was not invoked. On 28 November 2026, a Gradle test of odisee26 failed on the machine of the owner with "Timeout waiting to lock journal cache". Both odisee26 and erechnung mounted `$HOME/.gradle` as the Gradle user home of their containers. The owner chose one Gradle cache for each project.

## Develop

`jvm.mk` of `r-jvm` has the variable `GRADLE_CACHE`, which is `$HOME/.gradle/projects/<NAME>` by default. `GRADLE_RUN` mounts it as `/gradle`. The Gradle blocks of `templates/ci.yml` of `r-github-pipeline` save and restore `~/.gradle/projects/*/caches` and `~/.gradle/projects/*/wrapper`. `references/workflow.md` says so. The new row is [R-159](../requirements/jvm.md#r-159).

## Review

`TOOLS=host make gates` passed in the cloud session. 279 tests passed, and 1 of them is new. Podman and Gradle did not run, because the cloud session has neither.

## Release

Ships with the merge of the pull request by the owner and a tag.
