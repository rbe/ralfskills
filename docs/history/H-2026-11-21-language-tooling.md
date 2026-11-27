---
id: H-2026-11-21-language-tooling
title: Python, Gradle, and Go have a tooling target like Node
status: closed
adrs: []
skills: [develop, review, record, project-setup, python, jvm, go, shell]
decisions: []
proposals: []
issues: []
---

# Python, Gradle, and Go have a tooling target like Node

## Plan

`plan` was not invoked. The owner asked for the same target as `make node-tooling` for Python, JVM, and Go. Each language skill owns its Makefile template.

## Develop

`make python-tooling`, `make jvm-tooling`, and `make go-tooling` write the missing config files and `.gitignore` lines, then run `make format-fix`. The JVM target writes build files before the wrapper. The Go target runs `go mod init`. [R-66](../requirements/collection.md#r-66) states the targets. Shell is the language skill.

## Review

Gates passed in Podman. Each target ran in a new directory, and a second run changed no file. Security: each target runs its tools in Podman. No finding.

## Release

The branch is pushed and merged into the default branch with a pull request, after the owner confirmed. This collection publishes no image.
