---
name: security
description: Ask before a slice is closed, and check after implementation, when the change listens, stores a secret, accepts input, or runs a command. plan asks the questions. review runs the checks. Skip with the line "security: not installed" only when this skill is not installed.
kind: check
order: 10
---

# Security

## Steps

1. If `docs/BUGS.md`, `docs/WAVES.md`, `docs/FEATURES.md`, `docs/bugs/`, `docs/waves/`, or `docs/features/` exists, stop. Name `migrate-docs`. Do not take a later step.
2. Invoke `record` before creating an id or a document. A write that skips `record` fails this step.
3. Answer the questions when `plan` calls, or run the checks when `review` calls.
4. Ask `record` to add one line under the open history section naming `security`. Do not open a second history file.

Podman, XDG paths, and what a shipment may contain are `project-setup`. This skill does not restate them.

## Questions for plan

Ask these before the slice is closed. `plan` follows `order` on the skill index, so these come first.

1. What crosses a trust boundary: a listener, a file, a secret, or a command?
2. Who can call it?
3. What happens when the check says no?

## Checks for review

1. A secret is not in the tree, a log, an error, or a fixture.
2. A listener is the one the accepted ADR names.
3. Input has a bound on size and on type.
4. A command the program runs is the one the slice named.
