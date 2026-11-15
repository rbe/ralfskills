---
name: node
description: Node and TypeScript. Use when node is installed and the files in hand are JavaScript or TypeScript. Tests and installs run through make. A framework named in CLAUDE.md is a reference file beside this skill. The stage skill still applies.
---

# Node

## Steps

1. If `docs/BUGS.md`, `docs/WAVES.md`, `docs/FEATURES.md`, `docs/bugs/`, `docs/waves/`, or `docs/features/` exists, stop. Name `migrate-docs`. Do not take a later step.
2. Invoke `record` before creating an id or a document. A write that skips `record` fails this step.
3. Do the work below. `develop` invokes this skill for JavaScript and TypeScript files.
4. Ask `record` to add one line under Develop naming `node`. Do not open a second history file.

## Work

1. `make test` runs the tests. `make setup` installs dependencies. Do not run the package manager from a workflow step.
2. The language is TypeScript when the project already uses it. A new file follows that choice.
3. When `CLAUDE.md` names a framework, read `references/` beside this skill for that name. The framework file does not replace this skill or the stage skill.
4. Podman, XDG paths, and what a shipment may contain are `project-setup`.
