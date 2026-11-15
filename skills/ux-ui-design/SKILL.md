---
name: ux-ui-design
description: Ask before a slice is closed, and check after implementation, when the change has a screen, a control, or a visual. plan asks the questions. review runs the checks. Product tokens stay in a project skill. Skip with the line "ux-ui-design: not installed" only when this skill is not installed.
kind: check
order: 30
---

# UX and UI

## Steps

1. If `docs/BUGS.md`, `docs/WAVES.md`, `docs/FEATURES.md`, `docs/bugs/`, `docs/waves/`, or `docs/features/` exists, stop. Name `migrate-docs`. Do not take a later step.
2. Invoke `record` before creating an id or a document. A write that skips `record` fails this step.
3. Answer the questions when `plan` calls, or run the checks when `review` calls.
4. Ask `record` to add one line under the open history section naming `ux-ui-design`. Do not open a second history file.

This skill is interaction. A product's tokens, type scale, and component catalogue stay in a project skill named from `CLAUDE.md`.

## Questions for plan

1. What does the person do, in one sentence?
2. What does the empty state show, and what does the error state show?
3. Can a keyboard reach every control a pointer can reach?

## Checks for review

1. The screen matches the answers, including the empty state and the error state.
2. Focus is visible, and contrast holds for the text the person must read.
3. A token that belongs to one product was not copied into this skill.
