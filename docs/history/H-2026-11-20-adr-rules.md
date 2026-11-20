---
id: H-2026-11-20-adr-rules
title: Require the ADR rules and remove the wording tests
status: started
adrs: []
skills: [record, python]
decisions: [D-4, D-5]
proposals: []
issues: []
---

# Require the ADR rules and remove the wording tests

## Plan

`plan` was not invoked. The owner named the four rows and the removal.

Boundary: `docs/REQUIREMENTS.md` owns the statements. The skills do not say R-53 to R-56 yet. D-4 stays Open until they do.

Pattern: one row per rule. `plan` asks for the ADR. `develop` and `review` read it. `record` owns the status.

## Develop

R-53 to R-56 are rows in `docs/REQUIREMENTS.md`. `tests/test_skills.py` and `tests/test_integration.py` are deleted. `UNIT_TESTS` names the two script test files. `INTEGRATION_CMD` is `true`, because there is no integration entry. `.coveragerc` no longer names `tests`. One script test asserted a deleted test name and an empty list of ids with no test. Those two assertions are removed. The script test that required a test for every requirement is removed. The project report now lists R-4, R-5, R-7 to R-12, R-14, R-15, and R-53 to R-56 as ids with no test. Python is the language skill.

## Review

`make lint`, `make test`, and `make ids` were not run. This machine has no Podman. The two script test files and the id check were run with the host `python3`, and they passed.

security: no listener, no secret, no personal data in a fixture.

privacy: no personal data.

ux-ui-design: no screen.

api-design: not HTTP. Not a module export.

No finding. Left alone: the skill text for R-53 to R-56, the status filter in the project report, and the rows R-16 to R-52 of the owner's list.

## Release

Not invoked: this slice does not ship.
