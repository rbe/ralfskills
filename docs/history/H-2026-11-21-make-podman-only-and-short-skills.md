---
id: H-2026-11-21-make-podman-only-and-short-skills
title: Make and Podman as the only interface, general rules, and short skills
status: closed
adrs: []
skills: [develop, review, record, project-setup, python, shell]
decisions: [D-15, D-16]
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

Skills. All 20 `SKILL.md` files have the new shape: the one line, then tags and no heading. 20 new reference files hold the tables, the variable lists, and the rules for one condition. The 20 `SKILL.md` files had 19421 words and now have 10106 words. The new reference files have 6021 words. [R-76](../REQUIREMENTS.md#r-76) states the shape.

The last agent removed five things that still stood in two or more skills:

- The step "if `plan` calls, ask the questions" of the four subskills. `plan` step 2 and `review` step 1 already say it.
- The step that asks `record` for one line under Develop, in `go`, `jvm`, and `python`. The general rules say it.
- The sentence that a tooling target is safe to run again, in `go`, `jvm`, and `python`. It is now in step 4 of setup mode in `project-setup`.
- The name `index.mk` in `migrate-docs`. `record` names its own file.
- The sentence that `test-changed` is not a CI target, in `develop`. `review` step 10 keeps it.

The last agent also changed these texts. Step 5 of `plan` has the words of [R-14](../REQUIREMENTS.md#r-14) again. Report mode of `project-setup` and of `github-pipeline` reads `.DEFAULT_GOAL` in the makefiles and no longer runs `make -qp`. `python` and [R-66](../REQUIREMENTS.md#r-66) name both patterns of `UNIT_TESTS` in the template. `project-report` says that a test with an unknown id fails the target. The general rules say that `onboard` invokes `migrate-docs` itself, and that a skill adds no history line when no history file is open.

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
- The general rules say that the owner creates a `v*` tag and a skill creates none. `release`, `github-pipeline`, and `project-setup` dropped their copies.
- The README names the arguments for a proxy with its own CA and for a private repository beside the one `podman run` line.
- `review` step 10 makes only a `run:` step that is not `make <target>` a finding.
- `go` has `references/coverage.md` for the rules about `make coverage`, `make test-changed`, `make format`, and `make run`. The form of the `id:` line stands only in `record`. The `.gitignore` lines of a language stand only in its tooling reference.

Two parts of one finding were rejected. `github-pipeline` keeps "no Docker in place of Podman" and "calls no shell-script wrapper" in its top-level rules, because `references/contract.md` allows no divergence from a rule that stands there, and [R-40](../REQUIREMENTS.md#r-40) says that `github-pipeline` names Docker as not allowed. One finding asked to move the two sentences about the report skeleton to the general rules. They were deleted instead, because the skeleton itself states them.

Every gate passed through Make in Podman after the last edit: `make links`, `make format`, `make lint`, `make test` (76 tests), `make integration`, `make editorconfig`, `make coverage`, `make test-changed` (47 tests), `make ids`, `make toon`, `make links-check`, `make project-report`, and `make decision-log`. `build/coverage/diff.md` lists 250 changed lines and 2 lines that no test ran: line 60 of `project_report.py` and line 509 of `test_project_report.py`.

security: the cleanup targets pass `GH_TOKEN` or `GITHUB_TOKEN` from the environment to the container, and no file stores a token. The image of the GitHub CLI downloads the release archive with no checksum check. privacy: no personal data. ux-ui-design, api-design: not touched.

Not run: `gh api -X DELETE` and `gh release` against the real GitHub API, `make cleanup-container-versions` against the real API, `make build` of the Node pipeline template with the new smoke check, GNU Make 3.81, macOS, a GitHub Actions run, and rootful Podman. The bootstrap line and `make gh-image` ran only with a mount of the CA file of the session proxy. After the review fixes, these did not run: `make setup` of the Node and Gradle pipeline templates, `make setup` on a machine where Podman fails, and the bootstrap line with the new proxy arguments as the README now writes them.

Left alone:

- No agent ran a rewritten skill on a task. The texts were only read against the old texts.
- `block_lines` in `project_report.py` still reads the old headings "## Work" and "## Quality targets" when a tag is absent. No skill of the collection needs that now.
- `review` step 2 and `develop` step 3 skip the rule check in a repository that keeps no `docs/adr/`, as before. [R-54](../REQUIREMENTS.md#r-54) says so.
- No Make target reads a CI result or opens a pull request. `release` step 7 asks the owner for the CI result, and step 11 uses a pull request only if a Make target opens one. The owner must say whether `sdlc.mk` gets such targets.
- `templates/Makefile.node` of `github-pipeline` calls the host `tar` in four recipes to pack and unpack `node_modules`. The rule of `project-setup` allows `tar` by name as a tool of POSIX `sh`. The owner must say whether `tar` moves into the Node image.
- [D-5](../DECISIONS.md#d-5) says that this collection keeps no test on skill wording. The new shape tests check tags and one fixed line, and [R-28](../REQUIREMENTS.md#r-28) now says so.
- [D-16](../DECISIONS.md#d-16) is open: `make jvm-tooling` and a Kotlin build file.
- `CLAUDE.md` of `gh-sweep` still has the old paragraphs. Setup mode of `project-setup` now deletes a sentence that the general rules state, and [R-60](../REQUIREMENTS.md#r-60) says so.

## Release

The orchestrator commits the branch. The merge into the default branch waits for the owner.
