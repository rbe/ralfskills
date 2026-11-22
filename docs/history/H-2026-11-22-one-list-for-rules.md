---
id: H-2026-11-22-one-list-for-rules
title: One list for rules and one roadmap for work
status: started
adrs: [R-1, R-3, R-6, R-13, R-21, R-24, R-26, R-27, R-28, R-29, R-53, R-58, R-67, R-69, R-79, R-80, R-81, R-82]
skills: [develop, record, python]
roadmap: []
proposals: []
---

# One list for rules and one roadmap for work

## Plan

`plan` was not invoked. The owner decided the target model, and this slice implements it in the whole collection.

The owner decided these points:

- `docs/ROADMAP.md` holds the things to do in one table with the columns id, kind (feature, defect, or question), title, and proposal. The table has no status column. A row in the table is not done. `record` deletes the row and retires its id when the slice closes.
- `docs/proposals/<id>.md` is the detailed plan of one roadmap row.
- The rules in force are the ADRs in `docs/adr/` (product repositories only) and the rows of `docs/REQUIREMENTS.md`. This collection keeps only the rows.
- `docs/history/<id>.md` is the report of one slice. It is complete at any time and holds nothing that waits for a decision or for work.
- The code and the tests are the current state. A test names the rule it proves with `id:`.
- There is no `docs/DECISIONS.md` and no `docs/KNOWN_ISSUES.md`. A choice that must hold is a requirement row, a sentence in a fitting ADR, or a new ADR. If nothing fits, the agent asks the user. Not every choice is a rule.
- This collection has no roadmap. `docs/REQUIREMENTS.md` has a status column with the values `planned` and `in force`. A planned row is the open work or the open question, and a task that closes turns its row to in force or deletes it.
- `make old-board` names the two old files, and `migrate-docs` moves them and deletes them. The decision log goes away with the decisions.

The owner left the id form to the agent, to be chosen by the fewest words and the least code. The form is `W-` plus a number for every roadmap row. The column `kind` already holds feature, defect, or question, so a second form `K-` for a defect would add a kind to `id-kinds.md`, a template, and a sentence, and it would repeat the column. `ids.py`, `links.py`, and `report_links.py` read `[A-Z]-\d+`, so the form needed no new pattern.

Boundary: `record` writes every id and every board document. The scripts read the table rows and the frontmatter lists, and the skills hold steps and rules.

## Develop

The slice is five commits, and the first one holds more than the group 1 of the plan because the scripts, the rows, and the board data had to change together for the gates to pass.

- 51da799, `record`, `project-report`, and `board-merge-report`. `ids.py` and `links.py` read the rows of `docs/ROADMAP.md` and `docs/REQUIREMENTS.md`, and a frontmatter list may have the key `roadmap`. A history file written before may keep the keys `decisions` and `issues`. `requirements_index.py` writes the columns `id`, `title`, and `status`, and a row of a table with no status column is `in force`. `adr_index.py` writes the column `roadmap` in place of `decisions`. `decision_log.py`, its target `make decision-log`, and the templates `DECISIONS.md` and `KNOWN_ISSUES.md` are deleted. The template `ROADMAP.md` is a table. `references/close.md` deletes the roadmap rows that `roadmap:` of the history file names, and it turns the planned row of a task to in force in a repository with no roadmap. `references/adr.md` has the choice rule, and step 4 of write mode says that a repository with `docs/REQUIREMENTS.md` and no `docs/adr/` has only the row as its home. `requirements.py` of `project-report` has no decision kind and no issue kind, reads the roadmap table, and reads a planned row as work, not as a rule a test can name. The reviews list the roadmap rows and the planned rows. `board_numbers.py` leaves a planned row out of scope. The board data changed in the same commit. `docs/REQUIREMENTS.md` has the column Status, every earlier row is `in force`, and [R-79](../REQUIREMENTS.md#r-79) to [R-82](../REQUIREMENTS.md#r-82) are planned rows for D-19, D-23, D-22, and D-24. D-3 and D-21 are retired into [R-28](../REQUIREMENTS.md#r-28), D-20 into [R-53](../REQUIREMENTS.md#r-53), and R-62 is retired because it described only the decision log. `docs/DECISIONS.md` is deleted. [R-3](../REQUIREMENTS.md#r-3), [R-6](../REQUIREMENTS.md#r-6), [R-13](../REQUIREMENTS.md#r-13), [R-24](../REQUIREMENTS.md#r-24), [R-26](../REQUIREMENTS.md#r-26), [R-27](../REQUIREMENTS.md#r-27), [R-28](../REQUIREMENTS.md#r-28), [R-53](../REQUIREMENTS.md#r-53), [R-58](../REQUIREMENTS.md#r-58), [R-67](../REQUIREMENTS.md#r-67), and [R-69](../REQUIREMENTS.md#r-69) state the new behaviour.
- dbb28e2, the stage skills and the other skills. `plan` has the choice rule in step 6, the requirement-row branch of [R-53](../REQUIREMENTS.md#r-53), and a roadmap row for a proposal. `develop`, `review`, `release`, `project-report`, `system-state-report`, `onboard`, `board-merge-report`, `board-merge`, `node`, and `shell` name a roadmap row or a requirement row. [R-1](../REQUIREMENTS.md#r-1), [R-2](../REQUIREMENTS.md#r-2), [R-25](../REQUIREMENTS.md#r-25), [R-38](../REQUIREMENTS.md#r-38), [R-48](../REQUIREMENTS.md#r-48), [R-49](../REQUIREMENTS.md#r-49), [R-57](../REQUIREMENTS.md#r-57), [R-59](../REQUIREMENTS.md#r-59), [R-74](../REQUIREMENTS.md#r-74), [R-77](../REQUIREMENTS.md#r-77), and [R-78](../REQUIREMENTS.md#r-78) changed with them.
- d381228, `project-setup` and the entry files. `old-board.mk` lists eight paths. `CLAUDE.md` and the template of `project-setup` have the same board text in the `<general_rules>` block: a planned row of the requirements list replaces a roadmap row, and a test names an ADR id or a requirement id. [R-1](../REQUIREMENTS.md#r-1) and [R-21](../REQUIREMENTS.md#r-21) changed.
- 1e9cf79, `migrate-docs`. An Open row becomes a roadmap row of the kind question or feature, a known issue becomes a roadmap row of the kind defect, an old roadmap line becomes a roadmap row, and a Decided row goes where the choice rule of `record` says, with a question to the user where no home fits. The old labels are retired with `INTO=`, and a test that names an old label names the new id. `make old-board-delete` deletes the eight paths. [R-29](../REQUIREMENTS.md#r-29) changed.
- b3e9117, `README.md` has one table of the five board documents and no decision log, and `docs/REQUIREMENTS.md` says what the status column means.

Tests changed on the owner's decision. The three tests of `DecisionLogTest` and the two tests of `LinkTest` that read the decision log are deleted, because the log is deleted. The test of the report that pinned the sentence of D-3 now pins the heading `### Planned requirements` and the row [R-79](../REQUIREMENTS.md#r-79). The tests of the link, id, and board-number scripts use roadmap rows and planned rows in place of decision rows. New tests pin a roadmap row as a live id, the status column of the index, a planned row in the report, and a list with no status column. No test is skipped and none is weakened.

Numbers, read with Python in Podman through `make py`: `CLAUDE.md` has 759 words and the template has 830, inside the limits of 760 and 830. `docs/REQUIREMENTS.md` has 14050 words, 663 more than before, because each of 77 rows has the status and four rows are new. The 22 files `skills/*/SKILL.md` have 10820 words together.

Gates that ran after the last edit and passed: `make format`, `make lint`, `make test` with 102 tests, `make editorconfig`, `make ids`, `make toon`, `make links`, `make links-check`, `make integration`, `make coverage`, `make project-report`, `make old-board`, `make board-numbers`, and `make doctor`. `make coverage` reports 96 percent of the lines that differ from `origin/main`. The missing lines are in `ids.py` and `board_numbers.py`, and they came with earlier commits that are not pushed.

Not run: `make ci`, because this repository has no workflow and no such target.

## Review

Not invoked yet.

## Release

Not invoked: this slice does not ship.
