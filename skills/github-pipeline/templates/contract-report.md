# GitHub contract report

Skeleton for report mode. Fill a copy in the reply. Leave this file blank.

`State` is `matches` or `missing`. `Evidence` is a path, a variable, a hash, or a command. The verdict lists every row under one of those two words. A target is filled in when the Makefile gives it a recipe, or a command variable has a non-empty value. This report writes nothing in the project.

This is the contract report. It is not `build/report/index.md` from `make report`.

Project:

Skill: github-pipeline

## Verdict

Matches:

-

Missing:

-

## Applies

Make-only, this skill stays uninstalled: yes / no

Yes leaves the checks blank. No means the project publishes through GitHub, and the checks below are filled.

## Checks

The sha256 for `sdlc.mk` is the one in the Contract test section of `SKILL.md`.

| Check | State | Evidence |
| --- | --- | --- |
| Exactly one workflow, `.github/workflows/ci.yml`, named `CI` | | |
| Trigger is `push` on branches and `workflow_dispatch`. No `pull_request`. No tag trigger | | |
| Job ids and `needs` match the graph. `publish-*` needs `build` and `test` | | |
| Every `run:` step is `make <target>` | | |
| `publish-*` runs on the default branch or the dispatch input | | |
| Version comes from a `vMAJOR.MINOR.PATCH` tag via `make version` | | |
| `report` is last and has `!cancelled()` | | |
| Uploads set `retention-days`: 1 for intermediates, 14 for `report` and rendered docs | | |
| `sdlc.mk` is this skill's copy | | |
| The Makefile includes `sdlc.mk` before any target and leaves `project.mk` out | | |
| Runner is `ubuntu-26.04` | | |
| `AGENTS.md`, `docs/pipeline-rules.md`, `docs/BUGS.md`, `docs/WAVES.md`, `docs/FEATURES.md`, `Containerfile`, `.containerignore`, `.gitignore`, `Makefile`, `sdlc.mk`, and `.github/workflows/ci.yml` are present | | |
| Each divergence names the rule, what differs, and why. None is a match | | |
| No `.ONESHELL`, no Make 4 function, no shell-script wrapper. GNU Make 3.81 | | |

## Filled in

Setup mode leaves these recipes and these values.

| Target | Filled in | Where |
| --- | --- | --- |
| `setup` | | |
| `build` | | |
| `test` | | |
| `docs` | | |
| `login` | | |
| `publish-container` | | |
| `publish-github` | | |
