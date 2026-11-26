---
id: H-2026-11-26-r-publish-client
title: Add the publish-client workflow template
status: closed
adrs: [R-117, R-93, R-94]
skills: [r-record, r-github-pipeline]
roadmap: []
proposals: []
---

# Add the publish-client workflow template

## Plan

The owner asked for one generic template of the client workflow. `r-plan` was not invoked.

## Develop

[R-117](../requirements/github-pipeline.md#r-117) is the rule. `templates/publish-client.yml` keeps what the three projects share: tag `client-v*`, `workflow_dispatch`, version from `client/package.json`, `npm ci`, `npm test`, `npm pack`, a GitHub Release, and `npm publish` to GitHub Packages. Evidence: `dashboard/.github/workflows/publish-client.yml:10-14`, `reelbox/.github/workflows/publish-client.yml:7-12`, `ernaehrung/.github/workflows/publish-client.yml:7-12`. Setup mode step 5 copies it. [R-93](../requirements/github-pipeline.md#r-93), [R-94](../requirements/github-pipeline.md#r-94), `contract.md`, and the report skeleton allow it.

## Review

`make editorconfig`, `format`, `lint`, `test` (170 tests), and `coverage` (100%) passed. `make integration` is `true`. No workflow ran on GitHub.

## Release

Not invoked: this slice does not ship.
