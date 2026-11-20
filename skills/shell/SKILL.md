---
name: shell
description: POSIX shell inside a Make recipe. Use when shell is installed and the change is a recipe or a shell command. Make 3.81 rules are project-setup. Do not add a shell-script wrapper. The stage skill still applies.
kind: language
files: [sh]
names: [Makefile]
---

# Shell

## Steps

1. If `docs/BUGS.md`, `docs/WAVES.md`, `docs/FEATURES.md`, `docs/bugs/`, `docs/waves/`, or `docs/features/` exists, stop. Name `migrate-docs`. Do not take a later step.
2. Invoke `record` before creating an id or a document. A write that skips `record` fails this step.
3. Do the work below. `develop` invokes this skill for a recipe or a shell command.
4. Ask `record` to add one line under Develop naming `shell`. Do not open a second history file.

## Work

1. The shell is POSIX `sh`. A bash feature needs `CLAUDE.md` to name bash, and that choice is a Decided line through `record`.
2. The formatter is shfmt. The linter is shellcheck. They read `.sh` files. A project whose only shell is in Make recipes adds no shell formatter and no shell linter. Do not write a linter. Do not add a second formatter or a second linter for shell.
3. Recipe rules are `project-setup`: no `.ONESHELL`, no Make 4 function, no shell-script wrapper. Do not restate the rest of that contract.
4. `set -eu` starts a recipe that can fail. A shell `$` in a makefile is `$$`.
