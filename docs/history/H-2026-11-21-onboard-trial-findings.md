---
id: H-2026-11-21-onboard-trial-findings
title: Findings of the first agent trial of onboard
status: closed
adrs: []
skills: [develop, review, record, onboard, migrate-docs, project-setup, github-pipeline, python]
decisions: []
proposals: []
issues: []
---

# Findings of the first agent trial of onboard

## Plan

`plan` was not invoked. The owner asked for a fresh agent to run `report and integrate` on a Python project with an old board, a `src/` layout, and an image delivery. The agent reported 13 findings. Eleven are skill defects, one was already documented, and one is not a skill defect.

## Develop

- `migrate-docs` and `onboard` test the six old paths with `ls -d`. An empty directory counts, and Git does not list it. `migrate-docs` says what a new `CLAUDE.md` holds and where `project-setup` adds its paragraphs.
- `onboard` records the Decided rows of the existing tests in step 6, because setup mode needs them, and names the removal of the `__main__` block of a Python test.
- `python-tooling` also writes `*.pyc` and `.ruff_cache/` to `.gitignore`. The Ruff container writes `.ruff_cache/` as root.
- The `gitignore` template of `github-pipeline` has only the lines of every toolchain. Node and Gradle lines are comments.
- `Containerfile.python` shows the `src/` form. `Makefile.image` has the commented `OWNER` and `NAME` lines for a remote that is not on `github.com`. The intro of the `pipeline-rules.md` template no longer says that the project is the skill collection.
- `project-setup` report mode marks the Makefile rows `missing` when there is no Makefile.
- `onboard` step 10 reads the tags with `git ls-remote --tags` and carries the update steps, because the README of the collection is not installed.

Not changed: `make coverage` runs `git add -N .`. `project-setup` already says so. Make 3.81 is not checked on a machine that has Make 4: that is a limit of the test machine, not of a skill.

## Review

Every gate passed through Make in Podman. The agent ran onboard through every step with the installed skills and a local bare remote: five commits, and `make ci`, `make doctor`, `make build`, and all gates passed. It gave the first sentence the skills require. The `src/` layout and the image of a Python project worked, with `OWNER` and `NAME` set by hand. `python-tooling` was run again on a trial project, twice: the `.gitignore` has five lines, and the second run changed nothing.

security: no change in what runs. The `.gitignore` lines keep more generated files out of git.

privacy: no personal data.

ux-ui-design, api-design: not touched.

No finding. Left alone: the fixes were not tried by a second agent. No GitHub Actions run happened for the trial project. Make 3.81 was not available.

## Release

Merged into the default branch with a pull request after the owner confirmed. The owner named `v0.1.0` as the first tag.
