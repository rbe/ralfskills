# Make contract report

Skeleton for report mode. Fill a copy in the reply. Leave this file blank.

`State` is `matches` or `missing`. `Evidence` is a path, a variable, a hash, or a command. The verdict lists every row under one of those two words. A target is filled in when its command variable has a non-empty value, or the Makefile gives that target a recipe. This report writes nothing in the project.

Project:

Skill: project-setup

## Verdict

Matches:

-

Missing:

-

## Checks

The sha256 for `project.mk` is the one in the Check section of `SKILL.md`. A repository that includes `sdlc.mk` and leaves `project.mk` out matches that row: `sdlc.mk` already provides `help`.

| Check | State | Evidence |
| --- | --- | --- |
| `make` with no goal runs `help` | | |
| `project.mk` is this skill's copy, or `sdlc.mk` provides `help` and `project.mk` is absent | | |
| The include sits before any target (`project.mk`, or `sdlc.mk` when that file provides `help`) | | |
| `setup`, `build`, and `test` exist and are `.PHONY` | | |
| `docs` exists when the repository renders docs, and is absent otherwise | | |
| `login` exists when an image is published, and is absent otherwise | | |
| `SETUP_CMD`, `BUILD_CMD`, and `TEST_CMD` are non-empty | | |
| `DOCS_CMD` is non-empty when the repository renders docs | | |
| Gradle, npm, Podman, python, and tar run inside those targets | | |
| No `.ONESHELL`, no Make 4 function, no shell-script wrapper. GNU Make 3.81 | | |
| `setup` installs `jq` through Homebrew when `brew` is on `PATH` | | |

## Filled in

Setup mode leaves these recipes and these values.

| Target | Filled in | Where |
| --- | --- | --- |
| `setup` | | |
| `build` | | |
| `test` | | |
| `docs` | | |
| `login` | | |
