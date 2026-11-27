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

`plan` was not invoked. The request names the Open rows D-10 and D-11. `project-setup` owns setup mode.

## Develop

Setup mode asks how the project ships in step 1. The Go template has the variable `BIN`. With `BIN` set, `make build` writes `build/<name>`. `make run ARGS='...'` runs the program in the container. D-10 and D-11 are Decided rows now. [R-60](../requirements/project-setup.md#r-60) and [R-68](../requirements/go.md#r-68) state the rules.

## Review

Gates passed in Podman. In a new Go project, `make build` and `make run` worked with `BIN` set. With `BIN` empty, `make run` named `BIN` and failed. Security: no listener and no secret. No finding.

## Release

The branch is pushed and merged into the default branch with a pull request, after the owner confirmed. This collection publishes no image.
