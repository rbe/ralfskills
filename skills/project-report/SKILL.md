---
name: project-report
description: Generate the project report from the board and the tests. Use when the requirements-to-tests map, the architecture review, or the development review is needed. The report is a Make target. Hand-editing it is a defect.
---

# Project report

`make project-report` writes `build/project-report.md`. The file has the requirements-to-tests map, the architecture review, and the development review. Hand-editing it is a defect.

The map names which requirement id is proved by which tests, and which ids have no test. A requirement id is a roadmap id, a known-issue id, an ADR id, or a decision id. A test names that id with `id:` in its header or metadata, the line `record` matches.

The architecture review is drawn from the ADRs, the roadmap, known issues, and the checks in `plan` and `review`. The development review is drawn from the ADRs, the decisions, the roadmap, known issues, and the checks in `develop`, `review`, `release`, and `project-setup`.

## Steps

1. If `docs/BUGS.md`, `docs/WAVES.md`, `docs/FEATURES.md`, `docs/bugs/`, `docs/waves/`, or `docs/features/` exists, stop. Name `migrate-docs`. Do not take a later step.
2. Invoke `record` before creating an id or a document. A write that skips `record` fails this step.
3. Run `make project-report`. Stop when the target fails. Do not take a later step. Do not write `build/project-report.md` by hand.
4. Read the report. Stop when the requirements map, the architecture review, or the development review is missing. Do not take a later step. An id with no test is listed there. A test with no id fails the target.
5. Ask `record` to add one line under the open history section naming `project-report`. When no history file is open, do not open one.
