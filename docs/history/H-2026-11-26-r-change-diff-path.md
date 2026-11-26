---
id: H-2026-11-26-r-change-diff-path
title: Keep the change diff outside build/coverage
status: closed
adrs: [R-12]
skills: [r-project-setup]
roadmap: []
proposals: []
---

# Keep the change diff outside build/coverage

## Plan

The rollout of v0.7.0 to dashboard and ernaehrung found the defect. `r-plan` was not invoked.

## Develop

Vitest cleans `build/coverage/` when it starts, so it deleted the diff that `CHANGE_DIFF` wrote before `COVERAGE_CMD`, and diff-cover failed. `CHANGE_DIFF` now writes `build/change.diff`, and `DIFF_COVER` reads that file.

## Review

`make editorconfig`, `format`, `lint`, and `test` passed. A run of `CHANGE_DIFF` in a scratch repository wrote `build/change.diff`.

## Release

The owner merges the pull request and tags v0.7.1.
