---
id: H-2026-11-25-cover-ten-rows
title: Cover ten requirement rows that tests pin
status: closed
adrs: [R-1, R-2, R-3, R-6, R-13, R-28, R-69, R-76, R-77, R-84]
skills: [board-merge, board-merge-report, record, review]
roadmap: []
proposals: []
---

# Cover ten requirement rows that tests pin

## Plan

The owner merged PR 28 and asked to apply the action `cover` of `board-merge` to the rows [R-13](../requirements/record.md#r-13), [R-6](../requirements/record.md#r-6), [R-84](../requirements/record.md#r-84), [R-76](../requirements/project-setup.md#r-76), [R-69](../requirements/record.md#r-69), [R-3](../requirements/project-report.md#r-3), [R-2](../requirements/project-setup.md#r-2), [R-1](../requirements/record.md#r-1), [R-77](../requirements/board-merge-report.md#r-77), and [R-28](../requirements/record.md#r-28). A cover keeps the intent, the reason, and each fact that no test pins.

## Develop

Two agents applied the cover and made nine commits, one for each changed row. Only the files of `docs/requirements/` changed. No code and no test changed. No file of `docs/history/` was edited.

| Row | Words before | Words after |
| --- | --- | --- |
| R-13 | 328 | 328 |
| R-6 | 273 | 191 |
| R-84 | 211 | 182 |
| R-76 | 341 | 289 |
| R-69 | 199 | 143 |
| R-3 | 235 | 213 |
| R-2 | 297 | 276 |
| R-1 | 232 | 214 |
| R-77 | 441 | 398 |
| R-28 | 289 | 278 |

The words after come from `make board-numbers`. The rows together hold 2512 words after the cover.

[R-13](../requirements/record.md#r-13) has no commit. Only one sentence of the row is pinned by tests, and it has fewer than 10 words.

A third check read the diff of each row against the tests that carry the line `id:` of that row. Each deleted sentence has an assertion that pins it: the column lists of the three indexes and the file and owner columns ([R-6](../requirements/record.md#r-6)), the printed fields, the unknown id error, and the call with no variable ([R-84](../requirements/record.md#r-84)), the order of the general rules, the tag list, the closed tag rule, and the nesting rule ([R-76](../requirements/project-setup.md#r-76)), the plain text cases, the second run, and the anchor rule ([R-69](../requirements/record.md#r-69)), the report map and the hand-edit text ([R-3](../requirements/project-report.md#r-3)), the Node and JaCoCo grain ([R-2](../requirements/project-setup.md#r-2)), the path rule and the stop rule ([R-1](../requirements/record.md#r-1)), the columns of `make board-numbers` ([R-77](../requirements/board-merge-report.md#r-77)), and the missing `docs/REQUIREMENTS.md` and the two statuses ([R-28](../requirements/record.md#r-28)). No fact was restored. No other row or skill text points to a deleted fact.

## Review

The gates ran through Make in Podman. `make toon`, `make links`, `make ids`, `make links-check`, `make editorconfig`, `make format`, `make lint`, and `make test` passed after the last edit. `make test` ran 135 tests.

security, privacy, ux-ui-design, api-design: not touched.

Not run: `make integration` and `make coverage`.

## Release

Not invoked: the owner pushes this slice.
