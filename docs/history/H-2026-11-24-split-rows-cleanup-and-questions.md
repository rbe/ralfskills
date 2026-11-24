---
id: H-2026-11-24-split-rows-cleanup-and-questions
title: Split of R-45 and R-46, cleanup without a tag, the question rule, and the cover size limit
status: closed
adrs: [R-45, R-46, R-51, R-77, R-81, R-85, R-86, R-87, R-88, R-89, R-90, R-91, R-92, R-93, R-94, R-95, R-96, R-97, R-98, R-99]
skills: [record, develop, review, python, shell]
roadmap: []
proposals: []
---

# Split of R-45 and R-46, cleanup without a tag, the question rule, and the cover size limit

## Plan

The owner decided four points. R-81 is carried out by a split of [R-45](../requirements/project-setup.md#r-45) and [R-46](../requirements/github-pipeline.md#r-46) by topic. The cleanup targets must work at any time, with and without `DRY_RUN=1`, and must not need a `v*` git tag, so R-85 is carried out. The communication contract gets a rule for questions: the agent gives the context, and writes each id with its title and as a Markdown link. A cover finding has no size limit.

The owner asked why a cleanup target needs a `v*` tag. The target needed it because `SDLC_TAG` called `make version`, which reads the git tag and `GITHUB_RUN_NUMBER`. The kept version is now taken from a variable, a file, or the list from GitHub.

## Develop

Split of [R-45](../requirements/project-setup.md#r-45) and [R-46](../requirements/github-pipeline.md#r-46), in three commits before the question rule. [R-45](../requirements/project-setup.md#r-45) keeps the Make contract. [R-87](../requirements/project-setup.md#r-87) to [R-92](../requirements/project-setup.md#r-92) are new rows of `docs/requirements/project-setup.md`: setup mode and report mode ([R-87](../requirements/project-setup.md#r-87)), command variables ([R-88](../requirements/project-setup.md#r-88)), host tools in a recipe ([R-89](../requirements/project-setup.md#r-89)), targets of the Make contract ([R-90](../requirements/project-setup.md#r-90)), login and registry ([R-91](../requirements/project-setup.md#r-91)), and makefiles of skills and old board ([R-92](../requirements/project-setup.md#r-92)). [R-46](../requirements/github-pipeline.md#r-46) keeps the delivery contract. [R-93](../requirements/github-pipeline.md#r-93) to [R-99](../requirements/github-pipeline.md#r-99) are new rows of `docs/requirements/github-pipeline.md`: workflow and jobs ([R-93](../requirements/github-pipeline.md#r-93)), triggers and permissions ([R-94](../requirements/github-pipeline.md#r-94)), version and image tags ([R-95](../requirements/github-pipeline.md#r-95)), cleanup targets ([R-96](../requirements/github-pipeline.md#r-96)), divergences from the pipeline rules ([R-97](../requirements/github-pipeline.md#r-97)), targets and variables of `sdlc.mk` ([R-98](../requirements/github-pipeline.md#r-98)), and CI status and pull request targets ([R-99](../requirements/github-pipeline.md#r-99)). The counter `R` in `docs/ids.yaml` is 99. R-81 is deleted. The mentions in [R-75](../requirements/project-setup.md#r-75), [R-48](../requirements/review.md#r-48), and the test of the GitHub CLI name the new rows.

Cleanup without a git tag. `SDLC_TAG` in `skills/github-pipeline/sdlc.mk` no longer calls `make version`. The kept version is `PUBLISHED_TAG`, else the content of `build/publish-version.txt`, else the newest rolling version by `created_at` of the list from GitHub. A list with no rolling version deletes nothing and exits 0. A given tag that is not exactly one version in the list stops the target and names its source. [R-96](../requirements/github-pipeline.md#r-96) holds the rule. R-85 is deleted. Seven tests in `skills/project-report/scripts/test_project_report.py` run the real recipes against a fake GitHub CLI. `make links` un-linked the deleted ids R-81 and R-85 in two history files.

Question rule. The communication contract of `CLAUDE.md` and of `skills/project-setup/templates/CLAUDE.md` has the new group `Questions:` after the group `Content:`. It has three lines. Before a question, the agent gives the context and recommends one choice. The agent writes each id with its title and as a Markdown link, and `make req ID=<ids>` prints the title and the file. The user can answer without opening a file. The pinned word limits in the test of [R-76](../requirements/project-setup.md#r-76) went from 760 to 824 and from 830 to 894, which is 64 words each. [R-51](../requirements/collection.md#r-51) now has five parts and states the rule. The test `test_the_entry_file_and_its_template_hold_the_group_questions` names [R-51](../requirements/collection.md#r-51) and proves that both files hold the group in its place.

Cover size limit. [R-77](../requirements/board-merge-report.md#r-77), `skills/board-merge-report/SKILL.md`, and `skills/board-merge-report/references/finding-kinds.md` state that a cover finding has no size limit. [R-86](../requirements/board-merge-report.md#r-86) is rewritten to hold only the other question of the owner, on `make board-numbers`, with two choices.

## Review

Gates ran through Make in Podman after the last edit. `make lint` passed. `make test` passed with 133 tests. `make editorconfig` passed. `make format` failed once on the new test, `make format-fix` rewrote that file, and `make format` then passed. `make toon`, `make links`, `make ids`, and `make links-check` ran after the edits and passed.

A search of `README.md`, `CLAUDE.md`, and `skills/**/*.md` found no real id that is a bare id. Each hit is an example in a code span or the invented sample in `skills/board-merge-report/references/report-form.md`. A search of `skills/` for "question" and "ask" found no text that contradicts the question rule.

security, privacy, ux-ui-design, api-design: not touched.

Not run: a real GitHub Actions run, `make integration`, `make coverage`, and the cleanup targets against GitHub.

## Release

Not invoked: the owner merges and pushes this slice.
