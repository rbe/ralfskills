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

The owner decided two points, to make growing requirements cheap to read. First, `make req` prints one row, so that an agent does not read a whole file. Second, `docs/REQUIREMENTS.md` is split into one file for each skill that owns the row, in `docs/requirements/<skill>.md`. The owner of a row is the skill of its sentence `<skill> owns ...`. A row with several owners stands in the file of the skill whose rule it mainly states. A row with no owning skill stands in `collection.md`. The ids stay global and unchanged, and the rows [R-45](../requirements/project-setup.md#r-45) and [R-46](../requirements/github-pipeline.md#r-46) are not split by content.

## Develop

`docs/requirements/` has 23 files and the same 77 rows as before, plus the new row [R-84](../requirements/record.md#r-84). `docs/REQUIREMENTS.md` is deleted, and no stub stays, because no script or general rule needs that path. `make ids` fails when the old path exists, so that its rows do not stay unread.

`make req` is in `skills/record/index.mk`, with the script `skills/record/scripts/req.py`. It reads the rows of `docs/requirements/` and the ADRs of `docs/adr/`. It takes a variable only from the command line, because `OWNER` is also a variable of `github-pipeline`. It does not read `OWNER` for ADRs, does not rank, and does not read the roadmap or the proposals.

The scripts read the directory. `requirements_index.py` writes `docs/requirements-index.toon` with the columns `id`, `title`, `status`, `file`, and `owner`. `toon.py`, `links.py`, and `ids.py` read every file of the directory, so a link between rows in two files points to the other file. `requirements.py`, `report_links.py`, and `project_report.py` of `project-report` link each row to its own file. `board_numbers.py` counts the rows of every file.

The entry file, its template, the steps of `plan`, `develop`, and `review`, `record` with its references, `board-merge-report`, `system-state-report`, the README, and the rows [R-1](../requirements/record.md#r-1), [R-6](../requirements/record.md#r-6), [R-24](../requirements/record.md#r-24), [R-28](../requirements/record.md#r-28), [R-53](../requirements/record.md#r-53), [R-54](../requirements/develop.md#r-54), [R-3](../requirements/project-report.md#r-3), and [R-13](../requirements/record.md#r-13) now name `docs/requirements/`. The earlier history files keep the path of their time. `CLAUDE.md` has 759 words and the template has 830, inside the limits.

The tests that wrote `docs/REQUIREMENTS.md` write a file of `docs/requirements/` now, and they pin the new index columns and the new links. New tests cover `make req`, a link between two files, the rows of two files in `board_numbers.py`, the old path in `make ids`, and the layout of this repository.

## Review

Gates run through Make in Podman: `make format`, `make lint`, `make test` with 125 tests, `make editorconfig`, `make ids`, `make toon`, `make links-check`, `make coverage`, `make project-report`, `make board-numbers`, `make old-board`, and `make doctor`. `make -n req` also ran in GNU Make 3.81. security: no listener and no secret. privacy: no personal data. ux-ui-design and api-design: not touched.

## Release

Not invoked: the owner merges this slice.
