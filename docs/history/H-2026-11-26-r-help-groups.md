---
id: H-2026-11-26-r-help-groups
title: Group make help and move language targets into include files
status: closed
adrs: [R-11, R-122, R-66, R-116]
skills: [r-record, r-project-setup, r-github-pipeline, r-node, r-python, r-go, r-jvm]
roadmap: []
proposals: []
---

# Group make help and move language targets into include files

## Plan

The owner chose fixed help groups that show every target, and one include file for each language. `r-plan` was not invoked.

## Develop

[R-11](../requirements/project-setup.md#r-11) now has `help.mk` with `HELP_GROUPS` and `HELP_LIST`. `project.mk` and `sdlc.mk` run the list, and each makefile of the collection has `# help-group:` markers. [R-122](../requirements/collection.md#r-122) is new: `node.mk`, `python.mk`, `go.mk`, and `jvm.mk` hold the language targets, and the six templates include them. `podman-socket` is the version of `odisee26`. [R-66](../requirements/collection.md#r-66) and the skill texts name the new files. 17 tests are new.

## Review

`make editorconfig`, `format`, `lint`, `test` (195 tests), and `coverage` passed. `make integration` is `true`. `make help` ran here, and `make -n` ran on the six templates with GNU Make 4.3, not 3.81. `podman-socket` did not run.

## Release

Not invoked: this slice does not ship.
