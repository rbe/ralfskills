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

Both skills are registered in `CLAUDE.md`, in its template, in the README, and in [R-16](../REQUIREMENTS.md#r-16). The rows [R-77](../REQUIREMENTS.md#r-77) and [R-78](../REQUIREMENTS.md#r-78) and D-18 state the choice. The skill count in the shape test is 22. `CLAUDE.md` has 759 words and the template has 829, inside the limits of 760 and 830.

## Review

Trial: a copy of the repository ran both skills on real board text. The report listed 2 merges, 2 shortens, no cover, 1 history deletion, and no contradiction. Three findings were applied, each as one commit, and all gates passed after each commit. The trial found 15 points. Twelve were repaired: a history file is not edited or counted, a Decided row without a reason leaves no sentence, a Decided row with a unique sentence is a merge when the sentence moves, a repeat in one row is a shorten named `same row`, the Merge table has a column for the sentences to move, the Delete history table has words after, the report says which units it read, an absent `docs/adr/` is stated, the words after are measured before the commit, a deletion copies the reason as one sentence, the commit stages only the finding, and a failed gate leaves the edit in the working tree. Three were not defects: the file edit tool is allowed, `record` already covers a row edit, and staging with `git add` needs no Make target.

Every gate passed through Make in Podman after the repair. security: the script reads files and prints text, and it has no listener and no secret. privacy: no personal data. ux-ui-design, api-design: not touched.

Board repair, after the merge and shorten run. The commits since `1859147` retired 15 ids: R-15, D-5, D-6, and D-8 to D-18. They merged D-5 to D-18 and R-15 into other rows. They shortened rows in 38 commits. Two audits read the result. The first found no lost fact and no changed test. The second found contradictions between rows and the code. The repair fixed these points and changed no code and no test.

Restored facts. [R-46](../REQUIREMENTS.md#r-46) states again that no file of `github-pipeline` names `BUGS.md`, `WAVES.md`, or `FEATURES.md`, and that a Make-only repository does not install the skill. [R-60](../REQUIREMENTS.md#r-60) lists the other skills that the entry file names. [R-30](../REQUIREMENTS.md#r-30) states `checks: none installed` and that a row without a line fails the step. [R-57](../REQUIREMENTS.md#r-57) states that the owner creates a `v*` tag and a skill creates none.

Rows that the code showed false, now corrected. [R-11](../REQUIREMENTS.md#r-11) listed 7 makefiles that set `help` as the default goal, and 12 files do. [R-1](../REQUIREMENTS.md#r-1) said a test id on this collection is only a requirement row, and `requirements.py` also accepts a Decided row. [R-29](../REQUIREMENTS.md#r-29) said `make old-board-delete` checks the paths, and `migrate.mk` deletes them first. [R-44](../REQUIREMENTS.md#r-44) said `make` stays 3.81, and [R-73](../REQUIREMENTS.md#r-73) says 3.81 or newer. [R-63](../REQUIREMENTS.md#r-63) used a retired id as its example.

Duplicates and broken sentences removed. [R-40](../REQUIREMENTS.md#r-40) points to [R-75](../REQUIREMENTS.md#r-75) for the host rule and applies to both kinds of repository. The default of `OWNER` and `NAME` moved from [R-73](../REQUIREMENTS.md#r-73) to [R-71](../REQUIREMENTS.md#r-71). One sentence left each of [R-13](../REQUIREMENTS.md#r-13), [R-24](../REQUIREMENTS.md#r-24), [R-28](../REQUIREMENTS.md#r-28), and [R-48](../REQUIREMENTS.md#r-48), because another row states it. The second bullet of the section Discussed and not implemented left, because [R-57](../REQUIREMENTS.md#r-57) states it. [R-62](../REQUIREMENTS.md#r-62), [R-25](../REQUIREMENTS.md#r-25), and [R-27](../REQUIREMENTS.md#r-27) now say what the code and the neighbour rows say.

Words. `docs/REQUIREMENTS.md` and `docs/DECISIONS.md` had 13633 words at `1859147` and have 13071 now. The repair itself changed 13124 to 13071. `make board-numbers` counts 28456 words for 102 units, history files included, and this paragraph is part of that count.

## Waits for the owner

These rows stay unchanged, because they are in open owner questions or because the code does not decide.

- [R-3](../REQUIREMENTS.md#r-3) says a requirement id on this collection is a row of the requirements list. The code also accepts a Decided row. [R-3](../REQUIREMENTS.md#r-3) has a broken sentence that begins with `On a product repository and the two reviews`.
- [R-20](../REQUIREMENTS.md#r-20) says the general rules state that a non-stage skill opens no history file. The general rules do not state it. `record` does.
- [R-42](../REQUIREMENTS.md#r-42) lists 2 Containerfile templates, and the skill has 4. It also lists a shipment as a binary or an image, and [R-57](../REQUIREMENTS.md#r-57) adds the library package.
- [R-45](../REQUIREMENTS.md#r-45) forbids every host tool but `git` and `podman`. [R-75](../REQUIREMENTS.md#r-75) allows the tools of POSIX `sh`. [R-45](../REQUIREMENTS.md#r-45), [R-37](../REQUIREMENTS.md#r-37), [R-36](../REQUIREMENTS.md#r-36), and [R-39](../REQUIREMENTS.md#r-39) also repeat rules that other rows state.
- [D-3](../DECISIONS.md#d-3) says `in this list` and means the requirements list, but the Open and Decided rows live in `docs/DECISIONS.md`. A test in `test_project_report.py` pins the sentence, so the repair left it. It also repeats [R-28](../REQUIREMENTS.md#r-28). With [D-3](../DECISIONS.md#d-3) as the only row, the owner decides whether `docs/DECISIONS.md` goes, and where open work lives.
- The first bullet of Discussed and not implemented is a second home for a declined idea outside any row.
- Does [R-57](../REQUIREMENTS.md#r-57) keep that the merge itself asks no question? Old D-17 said so. `release` asks only before the ship.
- Seven history files name retired ids in `decisions:`. Leave them, or remove the ids?
- [R-45](../REQUIREMENTS.md#r-45) and [R-46](../REQUIREMENTS.md#r-46) hold 442 and about 790 words of unrelated facts. The owner decides whether to split them.

## Not run

The `cover` action never ran on real data, because the trial had no row with tests that pin every fact. Replacing an `id:` line of a test never ran, because no trial finding had a test on the retired id.

## Release

The merge into the default branch waits for the owner. The question whether a Decided row and a requirement row need to be two kinds is open.
