---
id: H-2026-11-20-adr-rules
title: Require the ADR rules and remove the wording tests
status: closed
adrs: [R-28]
skills: [plan, develop, review, record, project-report, python]
decisions: []
proposals: []
issues: []
---

# Require the ADR rules and remove the wording tests

## Plan

`plan` was not invoked. The owner named the four rows and the removal.

Boundary: `docs/REQUIREMENTS.md` owns the statements. The skills say [R-53](../REQUIREMENTS.md#r-53) to [R-56](../REQUIREMENTS.md#r-56). `plan` owns the request for an ADR. `develop` and `review` own the read. `record` owns the status and the divergence rule.

Pattern: one row per rule. `plan` asks for the ADR. `develop` and `review` read it. `record` owns the status.

## Develop

[R-53](../REQUIREMENTS.md#r-53) to [R-56](../REQUIREMENTS.md#r-56) are rows in `docs/REQUIREMENTS.md`. `tests/test_skills.py` and `tests/test_integration.py` are deleted. `UNIT_TESTS` names the two script test files. `INTEGRATION_CMD` is `true`, because there is no integration entry. `.coveragerc` no longer names `tests`. One script test asserted a deleted test name and an empty list of ids with no test. Those two assertions are removed. The script test that required a test for every requirement is removed. The project report now lists [R-4](../REQUIREMENTS.md#r-4), [R-5](../REQUIREMENTS.md#r-5), [R-7](../REQUIREMENTS.md#r-7) to [R-12](../REQUIREMENTS.md#r-12), [R-14](../REQUIREMENTS.md#r-14), R-15, and [R-53](../REQUIREMENTS.md#r-53) to [R-56](../REQUIREMENTS.md#r-56) as ids with no test. Python is the language skill.

[R-53](../REQUIREMENTS.md#r-53) is step 6 in `skills/plan/SKILL.md`, after the step that waits. [R-54](../REQUIREMENTS.md#r-54) is step 3 in `skills/develop/SKILL.md` and step 2 in `skills/review/SKILL.md`. [R-55](../REQUIREMENTS.md#r-55) is in that `review` step and in the ADRs section of `skills/record/SKILL.md`. [R-56](../REQUIREMENTS.md#r-56) is in that section, and `supersedes` is a link key. The project report does not list a superseded ADR as an id with no test. One script test names [R-56](../REQUIREMENTS.md#r-56). The open row D-4 is deleted and the id is retired.

## Review

`make lint`, `make test`, and `make ids` were not run. This machine has no Podman. The two script test files and the id check were run with the host `python3`, and they passed. The pinned Ruff image was not run. A host Ruff 0.16.9 reports the format check as clean. It reports 15 lint errors that the pinned 0.15.2 rules may not have. Thirteen are a shebang on a file that is not executable. None is on a line this change wrote.

security: no listener, no secret, no personal data in a fixture.

privacy: no personal data.

ux-ui-design: no screen.

api-design: not HTTP. Not a module export.

No finding. Left alone: the columns of `docs/adr/index.toon`, which do not list `supersedes`. The rows [R-16](../REQUIREMENTS.md#r-16) to [R-52](../REQUIREMENTS.md#r-52) of the owner's list. The open rows D-1 and D-2.

## Release

Not invoked: this slice does not ship.
