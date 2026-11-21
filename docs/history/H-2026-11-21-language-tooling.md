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

`plan` was not invoked. The owner asked for the same target as `make node-tooling` for Python, JVM, and Go. The one-run target of Node is the pattern.

Boundary: each language skill owns its Makefile template. `project-setup` owns the order of setup mode.

Pattern: one target per language sets up the tooling. It creates what is missing and leaves what is there.

## Develop

`make python-tooling`, `make jvm-tooling`, and `make go-tooling` are in the three templates. Each one writes the config files that are missing, `.editorconfig`, and the lines of `.gitignore`, and runs `make format-fix`.

Python has no manifest and no dependency to install, because Ruff and diff-cover are images. The target writes `.coveragerc`.

The JVM target writes `build.gradle`, `settings.gradle` with `NAME`, and the Checkstyle config before it writes the wrapper. The first version wrote the wrapper first, and Gradle failed, because `gradle wrapper` needs a settings file in the directory.

The Go target runs `go mod init` with `MODULE`. It runs `make format-fix` only when the project has a Go package, because `go list ./...` has nothing to list in a new project.

`python`, `jvm`, `go`, and step 3 of setup mode in `project-setup` name the targets. [R-66](../REQUIREMENTS.md#r-66) states them.

Shell is the language skill.

## Review

Every gate passed through Make in Podman with the pinned default images: `make format`, `make lint`, `make test`, `make integration`, `make editorconfig`, `make coverage`, `make test-changed`, `make ids`, `make toon`, `make links-check`, `make project-report`, and `make decision-log`.

Each target ran in a new directory with the template and the installed skills, in real Podman. After each run `make format`, `make lint`, and `make editorconfig` passed. A second run of each target changed no file. Go also ran again after a `main.go` was added.

security: each target runs its tools in Podman. The Gradle run downloads the Gradle distribution from `downloads.gradle.org`, and the Spotless and Checkstyle plugins from the plugin portal. The Go image and the Python image download nothing more. No listener, no secret.

privacy: no personal data.

ux-ui-design: no screen.

api-design: not HTTP. Not a module export. `NAME` and `MODULE` are the interface of the targets.

No finding. Left alone: the Python target was not run against a project with an old `pyproject.toml`. The JVM target was not run against a project that has a wrapper and no Checkstyle config. No trial agent used the targets. The sandbox of this session did not allow `downloads.gradle.org`. The owner added the host to the environment so the wrapper could be tested.

## Release

The branch is pushed and merged into the default branch with a pull request, after the owner confirmed. This collection publishes no image.
