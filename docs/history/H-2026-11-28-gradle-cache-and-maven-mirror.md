---
id: H-2026-11-28-gradle-cache-and-maven-mirror
title: Gradle cache and Maven mirror in the pipeline
status: started
adrs: [R-93, R-128, R-154]
skills: [github-pipeline, jvm, record]
roadmap: []
proposals: []
---

# Gradle cache and Maven mirror in the pipeline

## Plan

The owner asked why the odisee26 runs on `master` fail with HTTP 429 from Maven Central. The runs on `master` and on branches run the same jobs. Each job resolved every dependency again, because the workflow had no Gradle cache. No job passed `MAVEN_MIRROR` to Make. The owner then asked for the mirror and the cache in RalfSkills, so that each JVM project gets them. `r-plan` was not invoked, because the owner approved the scope in the chat.

## Develop

`templates/ci.yml` of `r-github-pipeline` has Gradle blocks. `setup` restores `~/.gradle/caches` and `~/.gradle/wrapper` and saves them after `make setup` when the key is new. `build` and `test` only restore them. The workflow `env` sets `MAVEN_MIRROR` from the repository variable. `references/workflow.md` has the rules, and the new row is [R-154](../requirements/github-pipeline.md#r-154). [R-93](../requirements/github-pipeline.md#r-93) names the cache steps as the only steps beside checkout, artifacts, and Make.

The init script `maven-mirror.gradle` of `r-jvm` adds the mirror and then the Gradle Plugin Portal when the settings file declares no plugin repository. Before, plugin dependencies such as `durian-core` still came from Maven Central, because the Plugin Portal redirects there. [R-128](../requirements/jvm.md#r-128) states the change.

## Review

Not invoked yet.

## Release

Not invoked yet.
