---
id: H-2026-11-20-go-format
title: gofmt reads the Go files of the project, and the Go caches belong to the project
status: closed
adrs: [R-60, R-68]
skills: [develop, review, record, go, shell]
decisions: []
proposals: []
issues: []
---

# gofmt reads the Go files of the project, and the Go caches belong to the project

## Plan

`plan` was not invoked. Two defects of the Go template are the input. One agent saw a Podman error while another container ran. A last agent, on a new Go project whose root is a package, found that gofmt read the whole tree.

Boundary: `go` owns its Makefile template.

Pattern: a command of the template reads the files of the project and no other file.

## Develop

The Podman error has a cause. In Podman 4.9.3, a container fails to start while another container holds the same named volume. Containers with different volumes run at the same time. The template gave every project the same two cache volumes. The volumes now have the name of the project directory.

`make format` and `make format-fix` gave gofmt the package directories. gofmt walks a directory, so with a package in the root it read `.claude/` and listed a file in a subpackage twice. The commands now give gofmt the Go files that `go list` names.

A last agent then ran on the branch with the volume change: a new Go project that ships a binary, with a feature that started at `plan`. It reports no blocker. Every Make target passed on the branch of the slice and on the default branch, and the binary gave the right output. Its one defect of a tool is the gofmt defect above. Two of its findings are not fixed here. They are the Open rows D-10 and D-11.

Shell is the language skill.

## Review

Every gate passed through Make in Podman with the pinned default images: `make format`, `make lint`, `make test`, `make integration`, `make editorconfig`, `make coverage`, `make test-changed`, `make ids`, `make toon`, `make project-report`, and `make decision-log`.

The gofmt change ran on a copy of the project of the last agent. `make format` passed with a badly formatted Go file inside `.claude/`. It failed and named the file once for a badly formatted file in a package. `make format-fix` repaired that file and did not change the file inside `.claude/`. The volume change ran on the code of `rbe/gh-sweep`, and every Go target passed.

security: no listener, no secret, no personal data in a fixture.

privacy: no personal data.

ux-ui-design: no screen.

api-design: not HTTP. Not a module export.

No finding. Left alone: the six minor findings of the last agent. No agent ran after the gofmt change.

## Release

The branch is pushed. The owner decides on the merge.
