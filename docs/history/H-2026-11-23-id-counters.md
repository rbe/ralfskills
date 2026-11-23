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

The owner decided three points. The owner asked whether a merged history is needed, because only `record` reads `docs/ids.yaml`. The owner chose one counter for each kind of id, and an id is never reused. The owner agreed to delete the section Discussed and not implemented, and the planned rows R-80, R-82, and R-83 left because these decisions settle them. The owner also asked that `make old-board` detect a `docs/ROADMAP.md` in the old line form. The owner said that this project has no users, so the change keeps no backward compatibility.

Declined: a wider `migrate-docs` that would read skills and other documents and would not delete the original project content, because the owner did not want it implemented.

## Develop

`docs/ids.yaml` holds one counter for each kind, one line `R: 83`. The counter is the highest number issued. The counters of this repository are R 83, W 0, ADR 14, P 0, and D 24. R 83 is the highest requirement id ever used. ADR 14 is the highest ADR id of the old retired list. D 24 is the highest id of the old decisions that history files still name.

`skills/record/scripts/ids.py` has no retired list and no map. `make id KIND=<kind>` prints the next id and raises the counter by one. `make id-raise KIND=<kind> TO=<number>` sets a counter to a higher number. `make ids-retire` is gone. `make ids` fails on a line of `docs/ids.yaml` that is not a counter, a list item that is not an id, an id above its counter, a live id that appears twice, and a counter below the highest live id. A history id has no counter. `links.py` no longer reads a retired list, so the id of a deleted row has no link target. The tests in `test_record.py` pin the new behaviour. The tests that pinned the retired list and the map were replaced, and no test was deleted without a replacement for its id.

`record`, `board-merge`, `board-merge-report`, `migrate-docs`, the references of `record`, the template of the roadmap, the README, and the rows [R-13](../REQUIREMENTS.md#r-13), [R-24](../REQUIREMENTS.md#r-24), [R-26](../REQUIREMENTS.md#r-26), [R-29](../REQUIREMENTS.md#r-29), [R-67](../REQUIREMENTS.md#r-67), [R-69](../REQUIREMENTS.md#r-69), [R-77](../REQUIREMENTS.md#r-77), and [R-78](../REQUIREMENTS.md#r-78) now say that a deleted row is gone. [R-13](../REQUIREMENTS.md#r-13) has the title Ids are never reused. `board_numbers.py` had no retired or merged logic, so only a comment changed. `make old-board` runs nine checks: the eight paths and a `docs/ROADMAP.md` with a line that starts with `- `. A unit test in `test_project_report.py` runs the check of the recipe in a shell on three cases. The texts of `migrate-docs`, the README, [R-21](../REQUIREMENTS.md#r-21), and [R-29](../REQUIREMENTS.md#r-29) say nine checks.

## Review

Gates run through Make in Podman: `make format`, `make lint`, and `make test`. Each result is in the commit message. security: no listener and no secret. privacy: no personal data. ux-ui-design and api-design: not touched.

Not run: `make integration` and `make coverage` have no entry in this repository.

## Release

Not invoked: the owner merges this slice.
