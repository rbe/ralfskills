---
id: H-2026-11-26-r-binary-smoke
title: Run a shipped binary once in the build
status: closed
adrs: [R-118]
skills: [r-record, r-go, r-github-pipeline]
roadmap: []
proposals: []
---

# Run a shipped binary once in the build

## Plan

The owner asked for a smoke rule for a project that ships a binary. `r-plan` was not invoked.

## Develop

[R-118](../requirements/go.md#r-118) is the rule, and `r-go` owns it. With `BIN` set, `make build` runs `build/<name> --help` in the Go image. Only `gh-sweep` ships a binary. It runs its image with `SMOKE_ARGS = --help` (`gh-sweep/Makefile:112`) and runs the built `bin/gh-sweep` nowhere. The collection already had `SMOKE_ARGS` in `container.mk`. The new part is the run of the binary itself. I checked the expansion with a small makefile for `GOOS` empty and set.

## Review

`make editorconfig`, `format`, `lint`, `test` (171 tests), and `coverage` (100%) passed. `make integration` is `true`. No Go project built with it.

## Release

Not invoked: this slice does not ship.
