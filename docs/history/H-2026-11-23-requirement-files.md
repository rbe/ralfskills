---
id: H-2026-11-23-requirement-files
title: One requirements file for each owning skill and make req
status: closed
adrs: [R-6, R-13, R-28, R-54, R-69, R-84]
skills: [develop, record, review, python, shell]
roadmap: []
proposals: []
---

# One requirements file for each owning skill and make req

## Plan

The owner chose two changes. `make req` prints one row, so an agent does not read a whole file. `docs/REQUIREMENTS.md` splits into one file for each owning skill, in `docs/requirements/<skill>.md`. Ids stay global. Rows [R-45](../requirements/project-setup.md#r-45) and [R-46](../requirements/github-pipeline.md#r-46) are not split.

## Develop

`docs/requirements/` has 23 files and 77 rows, plus the new row [R-84](../requirements/record.md#r-84). `make req` reads them through `skills/record/scripts/req.py`. The entry files and the skills name `docs/requirements/`. The rows [R-1](../requirements/record.md#r-1), [R-3](../requirements/project-report.md#r-3), [R-6](../requirements/record.md#r-6), [R-13](../requirements/record.md#r-13), [R-24](../requirements/record.md#r-24), [R-28](../requirements/record.md#r-28), [R-53](../requirements/record.md#r-53), and [R-54](../requirements/develop.md#r-54) name it too.

## Review

Gates passed in Podman, including `make test` with 125 tests, `make ids`, `make toon`, and `make project-report`. `make -n req` ran in GNU Make 3.81. Security, privacy, interaction, and API checks found nothing.

## Release

Not invoked: the owner merges this slice.
