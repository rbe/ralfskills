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

`plan` was not invoked. The project `rbe/gh-sweep` uses the skills on its default branch. Three slices ran there, and their findings are the input.

## Develop

Known issue K-1 was fixed at `develop`. A new agent fixed K-2 with the installed skills alone. A new flag ran from `plan` to `release`. The findings are fixed here: the Go coverage map selects a package whose tests run no statement, and `plan` asks what the result looks like. Python and shell are the language skills.

## Review

Gates passed in Podman with the pinned images. Security, privacy, interaction, and API checks found nothing. The fourth trial round stopped on the account usage limit.

## Release

The branch is pushed. This slice does not merge it.
