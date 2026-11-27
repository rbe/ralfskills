---
id: H-2026-11-24-split-rows-cleanup-and-questions
title: Split of R-45 and R-46, cleanup without a tag, the question rule, and the cover size limit
status: closed
adrs: [R-45, R-46, R-51, R-77, R-81, R-85, R-86, R-87, R-88, R-89, R-90, R-91, R-92, R-93, R-94, R-95, R-96, R-97, R-98, R-99]
skills: [record, develop, review, python, shell]
roadmap: []
proposals: []
---

# Split of R-45 and R-46, cleanup without a tag, the question rule, and the cover size limit

## Plan

[R-45](../requirements/project-setup.md#r-45) and [R-46](../requirements/github-pipeline.md#r-46) split by topic. Cleanup targets work without a `v*` tag. A contract rule covers questions. A cover finding has no size limit.

## Develop

Rows [R-87](../requirements/project-setup.md#r-87), [R-88](../requirements/project-setup.md#r-88), [R-89](../requirements/project-setup.md#r-89), [R-90](../requirements/project-setup.md#r-90), [R-91](../requirements/project-setup.md#r-91), and [R-92](../requirements/project-setup.md#r-92) belong to `project-setup`. Rows [R-93](../requirements/github-pipeline.md#r-93), [R-94](../requirements/github-pipeline.md#r-94), [R-95](../requirements/github-pipeline.md#r-95), [R-96](../requirements/github-pipeline.md#r-96), [R-97](../requirements/github-pipeline.md#r-97), [R-98](../requirements/github-pipeline.md#r-98), and [R-99](../requirements/github-pipeline.md#r-99) belong to `github-pipeline`. [R-48](../requirements/review.md#r-48) and [R-75](../requirements/project-setup.md#r-75) name them. `SDLC_TAG` no longer calls `make version`. [R-51](../requirements/collection.md#r-51) states the question rule. [R-76](../requirements/project-setup.md#r-76) raised the word limits. [R-77](../requirements/board-merge-report.md#r-77) states the cover rule. [R-86](../requirements/board-merge-report.md#r-86) keeps the open question.

## Review

Gates ran in Podman: `make lint`, `make test` (133 tests), `make editorconfig`, `make format`, `make links-check`, and `make ids` passed. Not run: a real GitHub Actions run, `make integration`, `make coverage`, and cleanup against GitHub.

## Release

Not invoked: the owner merges and pushes this slice.
