---
id: H-2026-11-20-ship-and-run
title: Setup asks how the project ships first, and a Go program runs with make run
status: closed
adrs: []
skills: [develop, review, record, project-setup, go, shell]
decisions: [D-10, D-11]
proposals: []
issues: []
---

# Setup asks how the project ships first, and a Go program runs with make run

## Plan

`plan` was not invoked. The request names the two Open rows D-10 and D-11.

Boundary: `project-setup` owns the order of setup mode. `go` owns its Makefile template.

Pattern: what an agent had to guess is a numbered step or a Make target.

## Develop

Setup mode asks how the project ships in step 1. It copies the Makefile template in step 2, and it sets the build command of a binary there. The entry file takes its ship sentence from the same answer.

The Go template has the variable `BIN`. With `BIN` set, `make build` writes `build/<name>` from `./cmd/<name>`, and `BIN_PKG` names another package. With `BIN` empty, `make build` compiles every package, as before. `make run ARGS='...'` compiles and runs the program in the Go container, with a terminal when Make has one. `GOOS` and `GOARCH` on the `make build` line give the binary of another machine.

D-10 and D-11 are Decided rows now. Each states the choice. [R-60](../requirements/project-setup.md#r-60) and [R-68](../requirements/go.md#r-68) have the new rules.

Shell is the language skill.

## Review

Every gate passed through Make in Podman with the pinned default images: `make format`, `make lint`, `make test`, `make integration`, `make editorconfig`, `make coverage`, `make test-changed`, `make ids`, `make toon`, `make links-check`, `make project-report`, and `make decision-log`.

The template ran in a new Go project with `BIN = hello`. `make build` wrote a Linux binary. `make run ARGS='a b'` printed the arguments. `make build GOOS=darwin GOARCH=arm64` wrote a macOS binary. With `BIN` empty, `make build` compiled the packages, and `make run` failed and named `BIN`. `make lint` and `make format` passed.

security: no listener, no secret. `ARGS` is what the person at the keyboard types, as in `make go`.

privacy: no personal data.

ux-ui-design: no screen.

api-design: not HTTP. Not a module export. `BIN`, `BIN_PKG`, and `ARGS` are the interface of the template.

No finding. Left alone: `make run` with a program that draws a screen was not run in a terminal here. No agent used the new step order in a trial. `rbe/gh-sweep` keeps its own Makefile and is not changed.

## Release

The branch is pushed and merged into the default branch with a pull request, after the owner confirmed. This collection publishes no image.
