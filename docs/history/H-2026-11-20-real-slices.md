---
id: H-2026-11-20-real-slices
title: Fix what the first slices in a real project found
status: closed
adrs: []
skills: [plan, develop, review, release, record, project-report, go, node, jvm, python, shell]
decisions: []
proposals: []
issues: []
---

# Fix what the first slices in a real project found

## Plan

`plan` was not invoked. The project `rbe/gh-sweep` uses the skills on its default branch. Three slices ran there, and their findings are the input of this slice.

Boundary: each stage owns its steps. `record` owns the layout of the history file. `project-report` owns the Go coverage map.

Pattern: what an agent had to guess in a real slice is now a sentence in the step that needed it.

## Develop

Three slices ran in `rbe/gh-sweep`.

- The fix of the known issue K-1 started at `develop`. The owner said to ship, and it is merged.
- A new agent, with no knowledge of this collection, fixed the known issue K-2 with the installed skills alone. It wrote a Go test that names ADR-0001. Its branch is pushed and closed on the board.
- A slice for a new flag started at `plan`, with the owner in the conversation and one question at a time. A second new agent then did `develop`, `review`, and `release` up to the merge, with Go code and eleven tests. Its review found an older defect of that project.

Their findings are fixed here. The Go coverage map lists a package with tests also when its tests ran no statement, so a change to a test file selects it. `release` says what to do when the owner merges later. `plan` asks what the result looks like, with the empty case and the error case, and it names each function the slice needs from a package the boundary keeps out. `plan` may ask the questions of a subskill after the slice is one sentence. `develop` needs no language row for a document. `record` says who is in `skills`, what `proposals` lists, and how a stage writes its section. The Makefile templates print the selected tests on one line.

Python and shell are the language skills.

## Review

Every gate passed through Make in Podman with the pinned default images: `make format`, `make lint`, `make test`, `make integration`, `make editorconfig`, `make coverage`, `make test-changed`, `make ids`, `make toon`, `make project-report`, and `make decision-log`.

security: no listener, no secret, no personal data in a fixture.

privacy: no personal data.

ux-ui-design: no screen.

api-design: not HTTP. Not a module export.

No finding. Left alone: the fourth trial round on sample projects. It stopped on the usage limit of the account. The slices in the real project gave the same kind of evidence with new agents.

## Release

The branch is pushed. This slice does not merge it.
