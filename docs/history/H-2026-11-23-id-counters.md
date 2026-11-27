---
id: H-2026-11-23-id-counters
title: Id counters replace the retired list
status: closed
adrs: [R-13, R-21, R-26, R-29]
skills: [develop, record, review, python, shell]
roadmap: []
proposals: []
---

# Id counters replace the retired list

## Plan

The owner chose one counter for each kind of id, and an id is never reused. No backward compatibility is kept. A wider `migrate-docs` was declined.

## Develop

`docs/ids.yaml` holds one counter for each kind. `make id KIND=<kind>` prints the next id. `make id-raise` sets a counter higher, and `make ids-retire` is gone. The rows [R-13](../requirements/record.md#r-13), [R-24](../requirements/record.md#r-24), [R-26](../requirements/record.md#r-26), [R-29](../requirements/migrate-docs.md#r-29), [R-67](../requirements/record.md#r-67), [R-69](../requirements/record.md#r-69), [R-77](../requirements/board-merge-report.md#r-77), and [R-78](../requirements/board-merge.md#r-78) say that a deleted row is gone. [R-21](../requirements/project-setup.md#r-21) says `make old-board` runs nine checks.

## Review

Gates ran in Podman: `make format`, `make lint`, and `make test`. Security, privacy, interaction, and API checks found nothing. Not run: `make integration` and `make coverage`.

## Release

Not invoked: the owner merges this slice.
