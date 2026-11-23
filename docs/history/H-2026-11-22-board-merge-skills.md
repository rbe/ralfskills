---
id: H-2026-11-22-board-merge-skills
title: The skills board-merge-report and board-merge
status: closed
adrs: [R-77, R-78]
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

Both skills are registered in `CLAUDE.md`, in its template, in the README, and in [R-16](../requirements/collection.md#r-16). The rows [R-77](../requirements/board-merge-report.md#r-77) and [R-78](../requirements/board-merge.md#r-78) and D-18 state the choice. The skill count in the shape test is 22. `CLAUDE.md` has 759 words and the template has 829, inside the limits of 760 and 830.

## Review

Trial: a copy of the repository ran both skills on real board text. The report listed 2 merges, 2 shortens, no cover, 1 history deletion, and no contradiction. Three findings were applied, each as one commit, and all gates passed after each commit. The trial found 15 points. Twelve were repaired: a history file is not edited or counted, a Decided row without a reason leaves no sentence, a Decided row with a unique sentence is a merge when the sentence moves, a repeat in one row is a shorten named `same row`, the Merge table has a column for the sentences to move, the Delete history table has words after, the report says which units it read, an absent `docs/adr/` is stated, the words after are measured before the commit, a deletion copies the reason as one sentence, the commit stages only the finding, and a failed gate leaves the edit in the working tree. Three were not defects: the file edit tool is allowed, `record` already covers a row edit, and staging with `git add` needs no Make target.

Every gate passed through Make in Podman after the repair. security: the script reads files and prints text, and it has no listener and no secret. privacy: no personal data. ux-ui-design, api-design: not touched.

Board repair, after the merge and shorten run. The commits since `1859147` retired 15 ids: R-15, D-5, D-6, and D-8 to D-18. They merged D-5 to D-18 and R-15 into other rows. They shortened rows in 38 commits. Two audits read the result. The first found no lost fact and no changed test. The second found contradictions between rows and the code. The repair fixed these points and changed no code and no test.

Restored facts. [R-46](../requirements/github-pipeline.md#r-46) states again that no file of `github-pipeline` names `BUGS.md`, `WAVES.md`, or `FEATURES.md`, and that a Make-only repository does not install the skill. [R-60](../requirements/project-setup.md#r-60) lists the other skills that the entry file names. [R-30](../requirements/plan.md#r-30) states `checks: none installed` and that a row without a line fails the step. [R-57](../requirements/release.md#r-57) states that the owner creates a `v*` tag and a skill creates none.

Rows that the code showed false, now corrected. [R-11](../requirements/project-setup.md#r-11) listed 7 makefiles that set `help` as the default goal, and 12 files do. [R-1](../requirements/record.md#r-1) said a test id on this collection is only a requirement row, and `requirements.py` also accepts a Decided row. [R-29](../requirements/migrate-docs.md#r-29) said `make old-board-delete` checks the paths, and `migrate.mk` deletes them first. [R-44](../requirements/project-setup.md#r-44) said `make` stays 3.81, and [R-73](../requirements/project-setup.md#r-73) says 3.81 or newer. [R-63](../requirements/project-report.md#r-63) used a retired id as its example.

Duplicates and broken sentences removed. [R-40](../requirements/project-setup.md#r-40) points to [R-75](../requirements/project-setup.md#r-75) for the host rule and applies to both kinds of repository. The default of `OWNER` and `NAME` moved from [R-73](../requirements/project-setup.md#r-73) to [R-71](../requirements/project-setup.md#r-71). One sentence left each of [R-13](../requirements/record.md#r-13), [R-24](../requirements/record.md#r-24), [R-28](../requirements/record.md#r-28), and [R-48](../requirements/review.md#r-48), because another row states it. The second bullet of the section Discussed and not implemented left, because [R-57](../requirements/release.md#r-57) states it. R-62, [R-25](../requirements/plan.md#r-25), and [R-27](../requirements/record.md#r-27) now say what the code and the neighbour rows say.

Words. `docs/REQUIREMENTS.md` and `docs/DECISIONS.md` had 13633 words at `1859147` and have 13071 now. The repair itself changed 13124 to 13071. `make board-numbers` counts 28456 words for 102 units, history files included, and this paragraph is part of that count.

## Rows corrected after the trial

The owner settled these points after the trial. This section states the results.

- [R-3](../requirements/project-report.md#r-3), [R-20](../requirements/record.md#r-20), [R-42](../requirements/github-pipeline.md#r-42), and [R-45](../requirements/project-setup.md#r-45) were corrected to what the skills and the code do. [R-57](../requirements/release.md#r-57) now says that the merge asks the owner nothing, and that `release` asks only before the ship.
- [R-36](../requirements/node.md#r-36), [R-37](../requirements/python.md#r-37), and [R-39](../requirements/jvm.md#r-39) keep framework detail in a reference file beside the language skill.
- D-3 says `in this list` and means the requirements list. A test in `test_project_report.py` pins the sentence.
- Thirteen history files name ids that were retired later. Their lists and their text are as they were written. `docs/ids.yaml` has the key `merged:`, which maps each id that a merge retired to the live ids that took its content. `make ids` checks that each id in a list is live or retired, and that each map line names a retired id and live ids. `make ids-retire` takes `INTO=` and rewrites no document.
- The work that these points left is in Open rows of `docs/DECISIONS.md`: D-19 moves the Node and Gradle templates of `github-pipeline` to command variables. D-20 adds the requirement-row branch to `plan` and `record`. D-21 decides whether `docs/DECISIONS.md` stays. D-22 decides where a declined idea lives. D-23 decides whether to split [R-45](../requirements/project-setup.md#r-45) and [R-46](../requirements/github-pipeline.md#r-46). D-24 makes `make board-numbers` follow the map.

## Not run

The `cover` action never ran on real data, because the trial had no row with tests that pin every fact. Replacing an `id:` line of a test never ran, because no trial finding had a test on the retired id.

## Release

Not invoked: the owner merges this slice.
