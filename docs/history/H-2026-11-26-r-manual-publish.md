---
id: H-2026-11-26-r-manual-publish
title: Publish large artifacts only by a human unless the project opts in
status: closed
adrs: [R-121, R-94, R-57]
skills: [r-record, r-github-pipeline, r-release, r-project-setup]
roadmap: []
proposals: []
---

# Publish large artifacts only by a human unless the project opts in

## Plan

The owner decided the rule to stay inside the GitHub quotas. `r-plan` was not invoked.

## Develop

[R-121](../requirements/github-pipeline.md#r-121) is the rule. In the three workflow templates, a `publish-*` job runs on a push to the default branch only when `vars.AUTO_PUBLISH == 'true'`, and always on `workflow_dispatch`. No Make target reads the flag. `publish-client.yml` stays tag and dispatch only. [R-94](../requirements/github-pipeline.md#r-94), [R-57](../requirements/release.md#r-57), `r-release`, the references, and the `CLAUDE.md` template changed. The template says `with a manual publish`.

## Review

`make editorconfig`, `format`, `lint`, `test` (178 tests), and `coverage` (100%) passed. `make integration` is `true`.

## Release

Not invoked: this slice does not ship.
