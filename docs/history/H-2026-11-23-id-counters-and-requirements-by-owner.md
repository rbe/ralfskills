---
id: H-2026-11-23-id-counters-and-requirements-by-owner
title: Repairs after the trials of the id counters and the requirement files
status: closed
adrs: [R-42, R-46, R-71, R-85, R-86]
skills: [develop, record, review, python, shell]
roadmap: []
proposals: []
---

# Repairs after the trials of the id counters and the requirement files

## Plan

The owner answered the open points. The id counters of `docs/ids.yaml` replace the retired list, and an id is never reused.

## Develop

`NAME` is derived once from the remote `origin`, or else from the directory name. `PACKAGE` defaults to `GITHUB_REPOSITORY`. `container.mk` passes `PODMAN_NET_ARGS` to `podman build`. [R-42](../requirements/github-pipeline.md#r-42), [R-46](../requirements/github-pipeline.md#r-46), and [R-71](../requirements/project-setup.md#r-71) say what the files now do. The new planned row [R-86](../requirements/board-merge-report.md#r-86) waits for an owner decision.

## Review

Gates passed in Podman, including `make test` with 125 tests and `make coverage`. Five trials ran on copies of real projects, and the cover findings were not applied. A real GitHub Actions run was not done.

## Release

Not invoked: the owner merges and pushes this slice.
