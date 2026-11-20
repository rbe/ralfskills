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

`plan` was not invoked. Two points were open after the previous slice. A JVM project on `project.mk` had no Makefile template. No new agent had confirmed the fixes for the findings of the second trial round.

Boundary: `jvm` owns the Makefile of a Gradle project, its build file, and its Checkstyle config. `project-setup` copies them.

Pattern: the same as for `python` and `node`. One template fills every command variable, and one Make target creates what a new project lacks.

## Develop

`jvm` has `templates/Makefile.gradle`, `templates/build.gradle`, and `templates/checkstyle.xml`. `$(GRADLE)` runs the Gradle wrapper in Podman. `make wrapper` writes the wrapper of a new project. Spotless runs google-java-format, Checkstyle is the linter, and JaCoCo feeds diff-cover and the coverage map.

Shell is the language skill.

## Review

Every gate passed through Make in Podman with the pinned default images and no override: `make format`, `make lint`, `make test`, `make integration`, `make editorconfig`, `make coverage`, `make test-changed`, `make ids`, `make toon`, `make project-report`, and `make decision-log`. Docker Hub accepted the pulls again.

The JVM template created a Gradle project through `make wrapper` and passed every target in Podman, in the images `gradle:9.1.0-jdk25` and `eclipse-temurin:25-jdk`. The diff report named the changed line that no test ran.

Three more agents ran a third trial round with the skills installed from this branch and the pinned default images: a new Gradle project, a new Node project, and an existing Python project with an old board. They did not read a script. All three report no blocker and say an agent can do the work with the installed skills alone. Each delivered its change, and every Make target passed in each project, on the branch of the slice and on the default branch after the merge. The Node and the Gradle project used their Makefile template with no change.

Their findings are fixed in this slice. Ruff does not read the installed skills. `record` says which names an ADR lists in `skills` and how the next id is chosen. `release` runs the gates before it closes the task. The default branch is the variable `DEFAULT_BRANCH`. The report lists only the lines of a roadmap, and lists a test file once for an id. `jvm` has a settings template, so the JAR has the name of the project. After these fixes, the three Makefile templates each ran a new sample project through every target in Podman again.

security: no listener, no secret, no personal data in a fixture. A template contains no credential.

privacy: no personal data.

ux-ui-design: no screen.

api-design: not HTTP. Not a module export.

No finding. Left alone: the versions in `templates/build.gradle` are in the build file. A project with a version catalog moves them there.

## Release

The branch is pushed and merged into the default branch with a pull request, after the owner confirmed. This collection publishes no image.
