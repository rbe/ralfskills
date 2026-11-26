---
id: H-2026-11-26-r-host-ports
title: Publish host ports above 1024 only
status: closed
adrs: [R-115]
skills: [r-record, r-github-pipeline]
roadmap: []
proposals: []
---

# Publish host ports above 1024 only

## Plan

The owner decided: a container may use a standard port inside, and a host binding uses a port above 1024. `r-plan` was not invoked.

## Develop

[R-115](../requirements/github-pipeline.md#r-115) is the rule, and `r-github-pipeline` owns it. `templates/Makefile.node` has `PORT` (inside) and `HOST_PORT` (host, default 8173). `run` fails when `HOST_PORT` is 1024 or lower. Evidence: `finanzdesk/Makefile:38-45` uses `RUN_HOST_PORT ?= 8443`.

## Review

`make editorconfig`, `format`, `lint`, `test` (168 tests), and `coverage` (100%) passed. `make integration` is `true`.

## Release

Not invoked: this slice does not ship.
