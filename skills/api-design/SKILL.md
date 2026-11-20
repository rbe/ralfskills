---
name: api-design
description: Ask before a slice is closed, and check after implementation, when the change adds or alters an HTTP route, a body, a status code, or what a module or a library exports. plan asks the questions. review runs the checks. The project's route catalogue stays in a project skill. Write the not-installed line only when this skill is not installed.
kind: check
order: 40
---

# API design

## Steps

1. If `docs/BUGS.md`, `docs/WAVES.md`, `docs/FEATURES.md`, `docs/bugs/`, `docs/waves/`, or `docs/features/` exists, stop. Name `migrate-docs`. Do not take a later step.
2. Invoke `record` before creating an id or a document. A write that skips `record` fails this step.
3. Answer the questions when `plan` calls, or run the checks when `review` calls.
4. Ask `record` to add one line under the open history section naming `api-design`. Do not open a second history file.

The list of routes for one product stays in a project skill named from `CLAUDE.md`. This skill is the shape of a change. HTTP is one part. The public API of a module or a library is the other part.

`api-design` asks what is exported, what stays internal, and what the resource, the verb, and the status on success are.

## Questions for plan

HTTP, when the slice changes a route. Otherwise answer `not HTTP`.

1. What is the resource, the verb, and the status on success?
2. What is the status and the error body on failure?
3. Which existing contract has to change in the same change as the handler?

A module or a library, when the slice changes what callers can import. Otherwise answer `not a module`.

4. What is exported?
5. What may a caller rely on?
6. What stays internal?

## Checks for review

Skip the HTTP checks when the answer was `not HTTP`. Skip the export checks when the answer was `not a module`.

1. The route matches the answers, including the failure status and the error body.
2. The contract and the handler changed together.
3. A new failure mode has a status and a body. A success body is not an error shape.
4. The export list matches the answers.
5. A caller relies only on what the answers named.
6. A name the answers called internal is not exported.
