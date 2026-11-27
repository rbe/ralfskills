---
id: H-2026-11-20-go-format
title: gofmt reads the Go files of the project, and the Go caches belong to the project
status: closed
adrs: []
skills: [develop, review, record, go, shell]
decisions: [D-10, D-11]
proposals: []
issues: []
---

# gofmt reads the Go files of the project, and the Go caches belong to the project

## Plan

`plan` was not invoked. A Podman error appeared when containers shared a volume. On a new Go project, gofmt read the whole tree.

## Develop

Podman 4.9.3 cannot start a container while another holds the same named volume. The template gave every project the same cache volumes, so the names now take the project directory name. `make format` gives gofmt only the Go files that `go list` names. Shell is the language skill.

## Review

Gates passed in Podman with the pinned images. A new agent trial found no blocker. Two of its findings stay open as D-10 and D-11. Security, privacy, interaction, and API checks found nothing.

## Release

The branch is pushed. This slice does not merge it.
