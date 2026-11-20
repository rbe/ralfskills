---
name: project-report
description: Generate the project report from the board and the tests. Use when the requirements-to-tests map, the architecture review, or the development review is needed. The report is a Make target. Hand-editing it is a defect.
---

# Project report

`make project-report` writes `build/project-report.md`. The file has the requirements-to-tests map, the architecture review, and the development review. Hand-editing it is a defect.

The map names which requirement id is proved by which tests, and which ids have no test. A superseded ADR is not listed as an id with no test. A requirement id is an ADR id or a decision id. A roadmap line and a known issue are work, not rules, and the map does not list them. The two reviews list them. When the repository keeps `docs/REQUIREMENTS.md` and does not keep `docs/adr/`, a requirement id is a row in that list. A test names that id with `id:` in its header or metadata, the line `record` matches. In a Python test the line is in the docstring of the test. In a JavaScript, TypeScript, Java, Groovy, or Kotlin test file the line is a comment, and the file is the proof. A test file with no id fails the target. An id with no test is listed and does not fail the target. `review` says whether that rule needs a test. A file under `.claude/`, `apm_modules/`, `node_modules/`, or `build/` is not a project test.

`report.mk` beside this skill sets `PROJECT_REPORT_CMD` when the project did not set it, and it owns the `project-report` target. `project.mk` and `sdlc.mk` include that file when this skill is installed.

The two reviews are lists, not a judgement. Each one puts the rules in force, the open work, and the numbered checks of the stages in one place, so that `review` reads one file. The architecture review is drawn from the ADRs, the roadmap, known issues, and the checks in `plan` and `review`. The development review is drawn from the ADRs, the decisions, the roadmap, known issues, and the checks in `develop`, `review`, `release`, and `project-setup`.

## Steps

1. If `docs/BUGS.md`, `docs/WAVES.md`, `docs/FEATURES.md`, `docs/bugs/`, `docs/waves/`, or `docs/features/` exists, stop. Name `migrate-docs`. Do not take a later step.
2. Invoke `record` before creating an id or a document. A write that skips `record` fails this step.
3. Run `make project-report`. Stop when the target fails. Do not take a later step. Do not write `build/project-report.md` by hand.
4. Read the report. Stop when the requirements map, the architecture review, or the development review is missing. Do not take a later step. An id with no test is listed there. A test with no id fails the target.
5. Ask `record` to add one line under the open history section naming `project-report`. When no history file is open, do not open one.
