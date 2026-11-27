---
id: H-2026-11-20-jvm-template
title: Give a Gradle project a Makefile template and confirm the fixes with new trials
status: closed
adrs: []
skills: [develop, review, record, project-setup, jvm, shell]
decisions: []
proposals: []
issues: []
---

# Give a Gradle project a Makefile template and confirm the fixes with new trials

## Plan

`plan` was not invoked. A JVM project on `project.mk` had no Makefile template, and no agent had confirmed the second round's fixes.

## Develop

`jvm` gained `templates/Makefile.gradle`, `templates/build.gradle`, and `templates/checkstyle.xml`. `make wrapper` writes the Gradle wrapper of a new project. Spotless, Checkstyle, and JaCoCo feed the format, lint, and coverage targets. Shell is the language skill.

## Review

Gates passed in Podman with the pinned images. A Gradle project from `make wrapper` passed every target. Three agents ran a third trial with the installed skills, and none reported a blocker. Their findings are fixed here. Left alone: the versions in `templates/build.gradle`.

## Release

The branch is pushed and merged into the default branch with a pull request, after the owner confirmed. This collection publishes no image.
