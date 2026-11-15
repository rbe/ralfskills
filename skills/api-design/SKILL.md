---
name: api-design
description: Ask before a slice is closed, and check after implementation, when the change adds or alters an HTTP route, a body, or a status code. plan asks the questions. review runs the checks. The project's route catalogue stays in a project skill. Skip with the line "api-design: not installed" only when this skill is not installed.
---

# API design

## Steps

1. If `docs/BUGS.md`, `docs/WAVES.md`, `docs/FEATURES.md`, `docs/bugs/`, `docs/waves/`, or `docs/features/` exists, stop. Name `migrate-docs`. Do not take a later step.
2. Invoke `record` before creating an id or a document. A write that skips `record` fails this step.
3. Answer the questions when `plan` calls, or run the checks when `review` calls.
4. Ask `record` to add one line under the open history section naming `api-design`. Do not open a second history file.

The list of routes for one product stays in a project skill named from `CLAUDE.md`. This skill is the shape of a change.

## Questions for plan

1. What is the resource, the verb, and the status on success?
2. What is the status and the error body on failure?
3. Which existing contract has to change in the same change as the handler?

## Checks for review

1. The route matches the answers, including the failure status and the error body.
2. The contract and the handler changed together.
3. A new failure mode has a status and a body. A success body is not an error shape.
