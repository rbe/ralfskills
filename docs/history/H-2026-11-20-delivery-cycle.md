---
id: H-2026-11-20-delivery-cycle
title: Complete the cycle, the decision records, and the requirements list
status: closed
adrs: []
skills: [plan, develop, review, release, record, project-report, project-setup, github-pipeline, security, privacy, python, shell]
decisions: [D-6]
proposals: []
issues: []
---

# Complete the cycle, the decision records, and the requirements list

## Plan

`plan` was not invoked. The owner set the goal: APM installs the skills, four stages deliver a change, and decisions form a record. `record` owns every board document.

## Develop

[R-1](../requirements/record.md#r-1) to [R-64](../requirements/project-report.md#r-64) are the requirement rows. [R-16](../requirements/collection.md#r-16) to [R-52](../requirements/collection.md#r-52) are the owner's list. [R-57](../requirements/release.md#r-57) to [R-64](../requirements/project-report.md#r-64) are new. `make decision-log` writes the decision log. Row D-7 was deleted. Python and shell are the language skills.

## Review

`make test`, `make integration`, `make ids`, `make toon`, `make project-report`, and `make decision-log` passed in Podman. `make lint`, `make format`, and `make editorconfig` ran outside Make, because the container network was blocked. No finding. [R-50](../requirements/plan.md#r-50) and [R-52](../requirements/collection.md#r-52) state rules that no skill states.

## Release

Not invoked: this slice does not ship. The branch is pushed. The owner merges.
