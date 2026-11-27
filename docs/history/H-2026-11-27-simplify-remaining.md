---
id: H-2026-11-27-simplify-remaining
title: The last ten findings of the simplification review
status: closed
adrs: [R-11, R-60, R-104, R-111, R-125, R-126]
skills: [plan, develop, review, record]
roadmap: []
proposals: []
---

# The last ten findings of the simplification review

## Plan

The owner answered twelve questions on findings 6, 8, 9, 10, 11, 12, 13, 15, 16 and 17 of the simplification review of 2026-11-26.

## Develop

`sdlc.mk` includes `project.mk` once. One `templates/ci.yml` replaces three. Node and Gradle use their language template plus `Makefile.image`. The upgrade skills became `references/upgrade.md`. One renderer replaces the project renderers ([R-125](../requirements/project-setup.md#r-125)). Images cover two platforms ([R-126](../requirements/github-pipeline.md#r-126)). 42 history files were shortened.

## Review

`make editorconfig`, `format`, `lint`, `test` (246 tests), `integration`, and `coverage` passed. Not run: a real two-platform build.

## Release

Pull request #42 merged as `4c028a8`, tagged v0.8.0. Seven project pull requests pin v0.8.0.
