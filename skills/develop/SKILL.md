---
name: develop
description: Implement a slice plan already closed, or a request that names a file or a failing test. Use the installed language skill for the files in hand. Two languages means two disjoint file sets. Stop when that language skill is not installed. Tests come with the behaviour change. Invoke record for ids and the Develop section.
---

# Develop

## Steps

1. If `docs/BUGS.md`, `docs/WAVES.md`, `docs/FEATURES.md`, `docs/bugs/`, `docs/waves/`, or `docs/features/` exists, stop. Name `migrate-docs`. Do not take a later step.
2. Invoke `record` before creating an id or a document. A write that skips `record` fails this step.
3. Do the work below, in order.
4. Ask `record` to write the Develop section, or one sentence that says why `develop` was not invoked. `record` rejects a history file missing Plan, Develop, Review, or Release.

## Work

1. Read the history file for this task. When the slice starts from a proposal, the Plan section cites that proposal id. Do not copy the proposal into Develop.
2. Read the installed language skill for the files in hand. `node`, `python`, `shell`, and `jvm` are the language skills. A file set with no installed language skill stops this step.
3. Two languages means two disjoint file sets. Finish one set before editing the other.
4. A behaviour change has a test. `make test` runs it. Podman, XDG paths, and what a shipment may contain are `project-setup`. Do not restate them.
5. An id, a roadmap line, or a known-issue change goes through `record`.
