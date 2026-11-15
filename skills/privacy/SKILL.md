---
name: privacy
description: Ask before a slice is closed, and check after implementation, when the change stores, logs, exports, or shows personal data. plan asks the questions. review runs the checks. Skip with the line "privacy: not installed" only when this skill is not installed.
kind: check
order: 20
---

# Privacy

## Steps

1. If `docs/BUGS.md`, `docs/WAVES.md`, `docs/FEATURES.md`, `docs/bugs/`, `docs/waves/`, or `docs/features/` exists, stop. Name `migrate-docs`. Do not take a later step.
2. Invoke `record` before creating an id or a document. A write that skips `record` fails this step.
3. Answer the questions when `plan` calls, or run the checks when `review` calls.
4. Ask `record` to add one line under the open history section naming `privacy`. Do not open a second history file.

## Questions for plan

Ask these with the security questions, before design or API questions.

1. What personal data is stored, shown, logged, or exported?
2. What remains if a log or a fixture is copied out of the machine?
3. Who asked for the export?

## Checks for review

1. Logs, errors, and fixtures contain no personal data.
2. An export is one the user asked for in this slice.
3. Example data is marked as an example. Real data is not in the tree.
