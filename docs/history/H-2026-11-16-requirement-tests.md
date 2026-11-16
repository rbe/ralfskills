---
id: H-2026-11-16-requirement-tests
title: Tests name requirements
status: started
adrs: [ADR-0001, ADR-0002, ADR-0003]
skills: [develop, review, project-setup, project-report, record, python, shell]
decisions: []
proposals: []
issues: []
---

# Tests name requirements

## Plan

The owner accepted three rules. A test names the requirement it proves with `id:` in its header or metadata, the same line `record` matches. The id is a roadmap id, a known-issue id, an ADR id, or a decision id. The test name states what the system does when that requirement holds. A test with no id fails review. The id is not a path.

`make test` stays the full suite and CI keeps running it. `make test-changed` runs the tests that cover the files in the diff, selected from coverage of those files. A green subset does not replace the full run.

`make project-report` writes the requirements-to-tests map, the architecture review, and the development review. Hand-editing that file is a defect.

Boundary: the board owns the requirement ids. A test names one of those ids. Coverage owns which test covers which file. The report reads both and is the only writer of `build/project-report.md`.

Pattern: `record` assigns ids. `make coverage` writes the coverage map. `make test-changed` reads that map and the diff. `make project-report` reads the board and the test headers. `make test` is the suite CI runs.

Standing rules the existing tests already proved are ADR-0004 through ADR-0013, so those tests can name an id.

## Develop

`project-report` generates the report. `develop`, `review`, `project-setup`, and `record` carry the rules as numbered steps. Python is the language skill for the report, the coverage map, and the selector. Shell is the language skill for the Make recipes. `make test` remains the full suite.

## Review

`make editorconfig`, `make format`, `make lint`, `make test`, `make integration`, `make coverage`, `make project-report`, and `make test-changed` passed. `make` with no target prints help.

security: the scripts read this repository and the coverage map. No listener, no secret, no personal data in a fixture.

privacy: no personal data.

ux-ui-design: no screen.

api-design: no HTTP route. The interface is the Make targets. The scripts stay internal.

No finding. Left alone: the CI workflows still run `make test` and do not run `test-changed`. The Node and Gradle templates are unchanged. The language skills are unchanged. diff-cover still reports the lines the change touched.

## Release

Not invoked: this slice does not ship.
