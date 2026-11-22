---
id: H-2026-11-22-board-merge-skills
title: The skills board-merge-report and board-merge
status: closed
adrs: []
skills: [develop, review, record, project-setup, board-merge-report, board-merge, python, shell]
decisions: [D-18]
proposals: []
issues: []
---

# The skills board-merge-report and board-merge

## Plan

`plan` was not invoked. The owner decided the scope, the four finding kinds, and the split into two skills.

Boundary: `board-merge-report` reads the board and writes nothing. `board-merge` writes the board only through `record`. The numbers come from one Make target, not from the agent.

Pattern: a script that prints one line for each unit, behind `make board-numbers`, included like `record/index.mk`. The two skills hold steps and rules, and the case detail is in reference files.

## Develop

The script `skills/board-merge-report/scripts/board_numbers.py` prints the id, the kind, the status, the words, the tests, the links, and the frontmatter lists for each requirement row, Decided row, ADR, and history file. `merge-report.mk` defines `make board-numbers` with `IDS=` to narrow the output. The root `Makefile`, `project.mk`, and `sdlc.mk` include it. The unit tests are in `test_board_numbers.py` and the root `Makefile` runs them.

Both skills are registered in `CLAUDE.md`, in its template, in the README, and in [R-16](../REQUIREMENTS.md#r-16). The rows [R-77](../REQUIREMENTS.md#r-77) and [R-78](../REQUIREMENTS.md#r-78) and [D-18](../DECISIONS.md#d-18) state the choice. The skill count in the shape test is 22. `CLAUDE.md` has 759 words and the template has 829, inside the limits of 760 and 830.

## Review

Trial: a copy of the repository ran both skills on real board text. The report listed 2 merges, 2 shortens, no cover, 1 history deletion, and no contradiction. Three findings were applied, each as one commit, and all gates passed after each commit. The trial found 15 points. Twelve were repaired: a history file is not edited or counted, a Decided row without a reason leaves no sentence, a Decided row with a unique sentence is a merge when the sentence moves, a repeat in one row is a shorten named `same row`, the Merge table has a column for the sentences to move, the Delete history table has words after, the report says which units it read, an absent `docs/adr/` is stated, the words after are measured before the commit, a deletion copies the reason as one sentence, the commit stages only the finding, and a failed gate leaves the edit in the working tree. Three were not defects: the file edit tool is allowed, `record` already covers a row edit, and staging with `git add` needs no Make target.

Every gate passed through Make in Podman after the repair. security: the script reads files and prints text, and it has no listener and no secret. privacy: no personal data. ux-ui-design, api-design: not touched.

## Not run

The `cover` action never ran on real data, because the trial had no row with tests that pin every fact. Replacing an `id:` line of a test never ran, because no trial finding had a test on the retired id.

## Release

The merge into the default branch waits for the owner. The question whether a Decided row and a requirement row need to be two kinds is open.
