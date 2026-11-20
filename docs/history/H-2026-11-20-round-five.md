---
id: H-2026-11-20-round-five
title: Fix what a fifth trial round found
status: closed
adrs: []
skills: [plan, develop, review, release, record, project-setup, migrate-docs, go, python, security, shell]
decisions: []
proposals: []
issues: []
---

# Fix what a fifth trial round found

## Plan

`plan` was not invoked. Two new agents ran a trial round with the skills installed by APM from the default branch. One set up a new Go project and delivered a feature that started at `plan`. One onboarded an existing Python project with an old board, fixed its open bug, and then delivered a feature that started at `plan` from a migrated proposal. Their findings are the input of this slice.

Boundary: each skill owns its steps and its templates. `project-setup` owns `project.mk`.

Pattern: what an agent had to choose is now a sentence or an example in the step that needed it.

## Develop

Both agents report no blocker. Both delivered each slice to the default branch, and every Make target passed in each project. Both say that `plan` made them ask what the result looks like, about the empty case, and about the error case. That was the first use of those questions.

Two defects of tools are fixed. The Go template built with an output directory, which fails for a library. It now compiles every package and writes no file. The pipe that put the selected tests on one line hid a missing coverage map, so `make test-changed` passed with no map. It fails again.

`make coverage` removes the report of an earlier run first. `release` names the form of the merge and the first line of the close commit. The roadmap template shows the line with two ids. `migrate-docs` says what a migrated proposal holds. `plan` says where the answers of a late grill go, and which choice about a library is an ADR. `develop` says that a method that rejects bad input and then computes does one thing. `review` gives one example of a rule that needs a test and one that does not. `python` says that a test file has no main block. `security` says that a type in a signature is the bound on type.

Shell is the language skill.

## Review

Every gate passed through Make in Podman with the pinned default images: `make format`, `make lint`, `make test`, `make integration`, `make editorconfig`, `make coverage`, `make test-changed`, `make ids`, `make toon`, `make project-report`, and `make decision-log`.

The two tool fixes ran on a copy of the Go trial project, which is a library. `make build` passed with the template unchanged. `make test-changed` failed with no coverage map. After `make coverage`, it selected the package of the changed file, and the diff report named the new lines no test ran.

security: no listener, no secret, no personal data in a fixture.

privacy: no personal data.

ux-ui-design: no screen.

api-design: not HTTP. Not a module export.

No finding. Left alone: the names of the Go cache volumes are the same for every project on a machine. One agent saw a Podman error while another container ran, and a second run passed. The cause is not known.

## Release

The branch is pushed. The owner decides on the merge.
