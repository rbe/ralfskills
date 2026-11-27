---
id: H-2026-11-19-collection-requirements
title: Record this collection as requirements
status: closed
adrs: []
skills: [record, plan, develop, review, project-report, python, shell]
decisions: [D-3]
proposals: []
issues: []
---

# Record this collection as requirements

## Plan

`plan` was not invoked. The request names the files and the recording rules. This collection's board owns the requirements list and the decisions list. Installed skills still own a product repository's roadmap and ADRs.

## Develop

`docs/ROADMAP.md` and `docs/adr/` are removed. Open work is an Open row in `docs/DECISIONS.md`. Each still-true ADR rule is one statement in `docs/REQUIREMENTS.md`. Python is the language skill for the index, the id check, and the report. Shell is the language skill for the Make include.

## Review

`make editorconfig`, `make format`, `make lint`, `make test`, `make integration`, `make coverage`, `make project-report`, `make test-changed`, `make ids`, and `make toon` passed. `make toon` wrote `docs/requirements-index.toon` and created no `docs/adr/`. No finding. A product repository with an ADR file keeps its ADR index.

## Release

Not invoked: this slice does not ship.
