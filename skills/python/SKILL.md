---
name: python
description: Python. Use when python is installed and the files in hand are Python. Tests run through make. Type hints are on public signatures. The stage skill still applies. A framework named in CLAUDE.md is not a reason to skip this skill.
kind: language
files: [py]
---

# Python

## Steps

1. If `docs/BUGS.md`, `docs/WAVES.md`, `docs/FEATURES.md`, `docs/bugs/`, `docs/waves/`, or `docs/features/` exists, stop. Name `migrate-docs`. Do not take a later step.
2. Invoke `record` before creating an id or a document. A write that skips `record` fails this step.
3. Do the work below. `develop` invokes this skill for Python files.
4. Ask `record` to add one line under Develop naming `python`. Do not open a second history file.

## Work

1. `make test` runs the tests. Dependencies resolve inside `make setup`.
2. Public functions have type hints. A module does one job.
3. A framework named in `CLAUDE.md` is read as a project skill. It does not replace this skill.
4. Podman, XDG paths, and what a shipment may contain are `project-setup`.
