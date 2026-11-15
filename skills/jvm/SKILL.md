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
2. `make test` runs the tests. `make build` runs Gradle. The workflow does not call Gradle itself.
3. Do not write a linter. Java's formatter is google-java-format and its linter is Checkstyle. Groovy's linter is CodeNarc. `make coverage` runs JaCoCo's XML through diff-cover. The report is the lines this change touched. Do not use a repository-wide percentage.
4. Podman, XDG paths, and what a shipment may contain are `project-setup`.
