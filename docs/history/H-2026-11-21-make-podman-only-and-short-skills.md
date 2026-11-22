---
id: H-2026-11-21-make-podman-only-and-short-skills
title: Make and Podman as the only interface, general rules, and short skills
status: closed
adrs: []
skills: [develop, review, record, project-setup, github-pipeline, release, python, shell]
decisions: [D-15, D-16, D-17]
proposals: []
issues: []
---

# Make and Podman as the only interface, general rules, and short skills

## Plan

`plan` was not invoked. The owner stated the goal and decided four things, and [D-15](../DECISIONS.md#d-15) records them:

1. The general rules stand once in `CLAUDE.md` and in the entry-file template of `project-setup`. Each `SKILL.md` refers to them in one line.
2. A person and an agent type only `make <target>` and Git commands. Every other tool runs behind a Make target in a Podman image. The host needs Make, Git, and Podman.
3. The first start is one `podman run` line in the README, because a project has no Makefile before the skills are installed.
4. Each `SKILL.md` keeps steps and rules in XML tags. Tables, samples, and rules for one condition move to reference files beside the skill.

Boundary: `CLAUDE.md` owns the rules for every skill. A `SKILL.md` owns only what that skill adds. `project-setup` owns the Make code for the host checks, for APM, and for the old board. `github-pipeline` owns the image of the GitHub CLI. `migrate-docs` owns the deletion of the old board.

Pattern: one fact in one place. A skill names the file of a rule and the condition under which the agent reads it.

## Develop

The work had three parts. A separate agent did each part, and one more agent joined the parts.

Interface. `skills.mk` in `project-setup` has `make skills-install`, `make skills-update`, and `make apm ARGS='...'`, which run APM 0.36.1 in a Python image. `old-board.mk` has `make old-board`. `migrate.mk` in `migrate-docs` has `make old-board-delete`. `make doctor` checks only Make, Git, Podman, and the remote `origin`. `make setup` installs nothing on the host, and Homebrew and jq are gone. `sdlc.mk` builds an image of the GitHub CLI with `make gh-image`, and the three cleanup targets and `_publish-github` of the Gradle template call the CLI in that image. The smoke check of the Node pipeline template runs curl in an image. The README has the one `podman run` line. [R-75](../REQUIREMENTS.md#r-75) states the interface.

General rules. `CLAUDE.md` and `skills/project-setup/templates/CLAUDE.md` have the same `<general_rules>` block with the parts Interface, Start of a task, Board, and Gates. `project_report.py` reads the numbered steps from the first `<steps>` block of a stage and from the first `<checks>` block of `project-setup`.

Skills. All 20 `SKILL.md` files have the new shape: the one line, then tags and no heading. 20 new reference files hold the tables, the variable lists, and the rules for one condition. The 20 `SKILL.md` files had 19218 words at commit 552ae7d and now have 10317 words. The 20 new reference files have 6109 words. `wc -w` counted all numbers. [R-76](../REQUIREMENTS.md#r-76) states the shape.

The last agent removed five things that still stood in two or more skills:

- The step "if `plan` calls, ask the questions" of the four subskills. `plan` step 2 and `review` step 1 already say it.
- The step that asks `record` for one line under Develop, in `go`, `jvm`, and `python`. The general rules say it.
- The sentence that a tooling target is safe to run again, in `go`, `jvm`, and `python`. It is now in step 4 of setup mode in `project-setup`.
- The name `index.mk` in `migrate-docs`. `record` names its own file.
- The sentence that `test-changed` is not a CI target, in `develop`. `review` step 10 keeps it.

The last agent also changed these texts. Step 5 of `plan` has the words of [R-14](../REQUIREMENTS.md#r-14) again. Report mode of `project-setup` and of `github-pipeline` reads `.DEFAULT_GOAL` in the makefiles and no longer runs `make -qp`. `python` and [R-66](../REQUIREMENTS.md#r-66) name both patterns of `UNIT_TESTS` in the template. `project-report` says that a test with an unknown id fails the target. The general rules say that `onboard` invokes `migrate-docs` itself, and that a skill adds no history line when no history file is open.

Owner decisions after the review, recorded in [D-17](../DECISIONS.md#d-17):

- `sdlc.mk` has `make ci-status`, `make pull-request`, and `make pull-request-merge`. All three run the GitHub CLI in the `gh-image` container with `-R owner/name` from `OWNER` and `NAME`, and with `--head` and `--base`. `ci-status` exits non-zero when the run failed, did not finish, or does not exist, and `WAIT=1` polls until the end. `pull-request-merge` merges with a merge commit when `gh pr checks` passes. `release` step 7 runs `make ci-status WAIT=1`. `release` step 11 runs `make pull-request` and `make pull-request-merge WAIT=1` when `.github/workflows` exists and `make help` lists the target, and otherwise makes a Git merge commit. [R-46](../REQUIREMENTS.md#r-46), [R-57](../REQUIREMENTS.md#r-57), and [R-75](../REQUIREMENTS.md#r-75) say so, and `references/makefile.md` of `github-pipeline` lists the targets.
- `tar` stays allowed as a tool of POSIX `sh`. The list stands once, in the Podman rule of `skills/project-setup/SKILL.md`, and `references/fail-list.md` no longer repeats it. The `tar` calls in `templates/Makefile.node` stay.
- `project-setup` keeps its behaviour for an existing `CLAUDE.md`: it deletes each sentence that the general rules state and names it in the reply. No text contradicted this, so no text changed.
- The general rules of `CLAUDE.md` and of its template say that, in a repository with `docs/REQUIREMENTS.md` and no `docs/adr/`, a step that names the ADR index reads `docs/requirements-index.toon` and opens the rows whose title the change touches. `develop` step 3 and `review` step 2 lost the sentences that skipped the step. [R-54](../REQUIREMENTS.md#r-54) says so.
- `CLAUDE.md` has 820 words and the template 881 (limits 850 and 900). At HEAD before this step they had 1359 and 1398 words, and at 552ae7d 708 and 807. `CLAUDE.md` plus the mean `SKILL.md` is 1335 words now and was 1668 at 552ae7d. The contract block keeps the three example pairs (active voice, condition first, specific noun) and is identical in both files. [R-76](../REQUIREMENTS.md#r-76) names the limits 850 and 900. Rules that one skill applies moved into that skill: modes (`project-setup`, `github-pipeline`), `<name>: not installed` (`plan`, `review`), one question at a time (`plan`), ids as plain text and one line from a non-stage skill (`record`), the `v*` tag (`release`), `test-changed` (`develop`), `make project-report` (`project-report`), one formatter and `format-fix` (`project-setup`). Unit tests for [R-2](../REQUIREMENTS.md#r-2) and [R-3](../REQUIREMENTS.md#r-3) now read those skills.

Tests for these decisions: `test_the_ci_result_and_the_pull_request_run_in_the_github_cli_image` pins the three recipes with [R-75](../REQUIREMENTS.md#r-75), and `test_a_requirements_repository_reads_the_requirements_index` pins the rule with [R-54](../REQUIREMENTS.md#r-54). No test was changed, deleted, or skipped.

Tests. Three tests pinned a general rule in a `SKILL.md`. They now pin the same sentence in the `<general_rules>` block of both entry files, because the rule moved. No test was deleted or skipped. New tests: seven for the interface, two for the general rules, and five for the shape of a skill. The shape tests check the one line, the tags, the reference file names, and that only `migrate-docs` names a path of the old board. Four tests name [R-75](../REQUIREMENTS.md#r-75) and [R-76](../REQUIREMENTS.md#r-76).

Requirement rows. [R-75](../REQUIREMENTS.md#r-75) and [R-76](../REQUIREMENTS.md#r-76) are new. These rows changed because the slice made a sentence false: [R-16](../REQUIREMENTS.md#r-16), [R-18](../REQUIREMENTS.md#r-18), [R-60](../REQUIREMENTS.md#r-60), [R-19](../REQUIREMENTS.md#r-19), [R-20](../REQUIREMENTS.md#r-20), [R-21](../REQUIREMENTS.md#r-21), [R-7](../REQUIREMENTS.md#r-7), [R-14](../REQUIREMENTS.md#r-14), [R-5](../REQUIREMENTS.md#r-5), [R-28](../REQUIREMENTS.md#r-28), [R-8](../REQUIREMENTS.md#r-8), [R-34](../REQUIREMENTS.md#r-34), [R-66](../REQUIREMENTS.md#r-66), [R-1](../REQUIREMENTS.md#r-1), [R-45](../REQUIREMENTS.md#r-45), [R-72](../REQUIREMENTS.md#r-72), and [R-73](../REQUIREMENTS.md#r-73).

python: the language skill for the tests and for `project_report.py`. shell: the language skill for the recipes.

## Review

Three reviewers read the finished slice: one for the interface, one as an agent with no context, and one for words and prompting. They gave 38 findings. A last agent checked each finding against the files. 37 findings led to a change. The finding about the host `tar` is a question for the owner, under what was left alone. These are the changes that alter what an agent or a target does:

- `doctor.mk` makes `doctor` the first prerequisite of `setup`. Before, `make setup` ran `toon` in Podman before `doctor`. `make setup` ran here and printed the `doctor` lines first. The unit test for [R-73](../REQUIREMENTS.md#r-73) now checks the prerequisite and the order of the includes, in place of the recipe line that it checked before.
- `report.mk` includes `podman-python.mk` when it runs alone. `make -f skills/project-report/report.mk project-report` ran here in Podman.
- `DOCTOR_SKIP_PODMAN` is gone.
- No divergence allows a host JDK or a host Python. `references/contract.md` of `github-pipeline`, the Gradle template, [R-40](../REQUIREMENTS.md#r-40), [R-43](../REQUIREMENTS.md#r-43), and [R-46](../REQUIREMENTS.md#r-46) no longer name one.
- `release` step 7 asks the owner for the CI result, because no Make target reads it.
- `onboard` reads the general rules from the entry-file template when `CLAUDE.md` does not have them. It runs `migrate-docs` also when only `AGENTS.md` exists. It says what it does when the project has no remote `origin`. It gives the URL form for `git ls-remote`. It no longer repeats steps of `project-setup`, `migrate-docs`, and `github-pipeline`.
- `project-setup` copies a Makefile template when the project has no Makefile, and it runs the tooling target when the Makefile came from a template in the run or when a file that the target writes is missing. The items of `<checks>` are statements that are true or false. The edits that make them true are in setup step 8.
- The ship sentence of the entry-file template has one option for each of the four answers.
- The rule that the owner creates a `v*` tag and a skill creates none stands in `release` only. `github-pipeline` and `project-setup` dropped their copies.
- The README names the arguments for a proxy with its own CA and for a private repository beside the one `podman run` line.
- `review` step 10 makes only a `run:` step that is not `make <target>` a finding.
- `go` has `references/coverage.md` for the rules about `make coverage`, `make test-changed`, `make format`, and `make run`. The form of the `id:` line stands only in `record`. The `.gitignore` lines of a language stand only in its tooling reference.

Two parts of one finding were rejected. `github-pipeline` keeps "no Docker in place of Podman" and "calls no shell-script wrapper" in its top-level rules, because `references/contract.md` allows no divergence from a rule that stands there, and [R-40](../REQUIREMENTS.md#r-40) says that `github-pipeline` names Docker as not allowed. One finding asked to move the two sentences about the report skeleton to the general rules. They were deleted instead, because the skeleton itself states them.

Every gate passed through Make in Podman after the last edit: `make links`, `make format`, `make lint`, `make test` (78 tests), `make integration`, `make editorconfig`, `make coverage`, `make test-changed` (49 tests), `make old-board`, and `make doctor`, `make ids`, `make toon`, `make links-check`, `make project-report`, and `make decision-log`. `build/coverage/diff.md` lists 288 changed lines and 2 lines that no test ran: line 60 of `project_report.py` and line 523 of `test_project_report.py`.

security: the cleanup targets pass `GH_TOKEN` or `GITHUB_TOKEN` from the environment to the container, and no file stores a token. The image of the GitHub CLI downloads the release archive with no checksum check. privacy: no personal data. ux-ui-design, api-design: not touched.

Not run: `gh api -X DELETE` and `gh release` against the real GitHub API, `make cleanup-container-versions` against the real API, `make build` of the Node pipeline template with the new smoke check, GNU Make 3.81, macOS, a GitHub Actions run, and rootful Podman. The bootstrap line and `make gh-image` ran only with a mount of the CA file of the session proxy. After the review fixes, these did not run: `make setup` of the Node and Gradle pipeline templates, `make setup` on a machine where Podman fails, and the bootstrap line with the new proxy arguments as the README now writes them.

Left alone:

- The sentence "CI runs the same six targets", the sentence that `make toon` writes the two index files, and the trigger "Say `state report`" of the template are gone from the entry files. The Podman rule already says "in CI", and the description of `system-state-report` holds "state report". The owner may ask for them back.

- No agent ran a rewritten skill on a task. The texts were only read against the old texts.
- `block_lines` in `project_report.py` still reads the old headings "## Work" and "## Quality targets" when a tag is absent. No skill of the collection needs that now.
- [D-5](../DECISIONS.md#d-5) says that this collection keeps no test on skill wording. The new shape tests check tags and one fixed line, and [R-28](../REQUIREMENTS.md#r-28) now says so.
- [D-16](../DECISIONS.md#d-16) is open: `make jvm-tooling` and a Kotlin build file.
- `CLAUDE.md` of `gh-sweep` still has the old paragraphs. Setup mode of `project-setup` now deletes a sentence that the general rules state, and [R-60](../REQUIREMENTS.md#r-60) says so.

## Release

The orchestrator commits the branch. The merge into the default branch waits for the owner.
