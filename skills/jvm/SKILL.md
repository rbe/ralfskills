---
name: jvm
description: Java, Groovy, Grails, and Gradle. Use when jvm is installed and the files in hand are Java, Groovy, Grails, or Gradle. Read the reference that matches the file. Tests run through make. The stage skill still applies.
kind: language
files: [java, groovy, gradle, kts]
---

# JVM

## Steps

1. If `docs/BUGS.md`, `docs/WAVES.md`, `docs/FEATURES.md`, `docs/bugs/`, `docs/waves/`, or `docs/features/` exists, stop. Name `migrate-docs`. Do not take a later step.
2. Invoke `record` before creating an id or a document. A write that skips `record` fails this step.
3. Do the work below. `develop` invokes this skill for Java, Groovy, Grails, and Gradle files.
4. Ask `record` to add one line under Develop naming `jvm`. Do not open a second history file.

## Work

1. Read the reference that matches the file: `references/java.md`, `references/groovy.md`, `references/grails.md`, or `references/gradle.md`.
2. `make test` runs the tests. `make build` runs Gradle. The workflow does not call Gradle itself. `templates/Makefile.gradle` beside this skill is the Makefile of a Gradle project on `project.mk`: `$(GRADLE)` runs the Gradle wrapper in Podman, and each command variable is filled in. `make wrapper` writes the Gradle wrapper of a new project. `templates/build.gradle`, `templates/settings.gradle`, and `templates/checkstyle.xml` are the build file, the settings file, and the Checkstyle config those commands need. `project-setup` copies them to `build.gradle`, `settings.gradle`, and `config/checkstyle/checkstyle.xml` when the project has none. Set the project name in `settings.gradle`, and the group and the version in `build.gradle`. Gradle names the JAR after them. Source is in `src/main/java`, and tests are in `src/test/java`. A new project has its build file from the template, so the one Make target it runs first is `make wrapper`. `.gitignore` has the lines `build/` and `.gradle/`. A test file names its requirement in a comment in the file header: `// id: D-1`, one line for each id.
3. Do not write a linter. Java's formatter is google-java-format and its linter is Checkstyle. Groovy's linter is CodeNarc. `make coverage` runs JaCoCo's XML through diff-cover. The report is the lines this change touched. Do not use a repository-wide percentage. `make coverage` also runs `jacoco_cover_map.py` from `project-report`. That script reads the JaCoCo execution data and writes the coverage map: each test class, and the source files that ran in its JVM. `make test-changed` gives the test classes that `changed_tests.py --print` names to Gradle with `--tests`.
4. Podman, XDG paths, and what a shipment may contain are `project-setup`.
