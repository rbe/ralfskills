---
id: H-2026-11-26-r-web-smoke
title: Check the page root in the smoke check of a web image
status: closed
adrs: [R-119]
skills: [r-record, r-github-pipeline]
roadmap: []
proposals: []
---

# Check the page root in the smoke check of a web image

## Plan

The owner asked to check the needle of the smoke check. `r-plan` was not invoked.

## Develop

[R-119](../requirements/github-pipeline.md#r-119) is the rule. The template checked only the API needle (`ok` on `/api/health`). Three projects also check the page `/` for `id="root"`: `dashboard/Makefile:107`, `ernaehrung/Makefile:106`, `finanzdesk/Makefile:166`. The template now has `SMOKE_PAGE_NEEDLE`, default `id="root"`, and an empty value turns the check off. The `SMOKE_NEEDLE` values of the projects stay project values: `not for git` (`dashboard/Makefile:22`), `eintraege` (`ernaehrung/Makefile:27`), and `http://localhost:11434` (`finanzdesk/Makefile:49`).

## Review

`make editorconfig`, `format`, `lint`, `test` (172 tests), and `coverage` (100%) passed. `make integration` is `true`. The image smoke did not run.

## Release

Not invoked: this slice does not ship.
