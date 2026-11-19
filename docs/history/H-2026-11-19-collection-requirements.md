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

`plan` was not invoked. The request names the files and the recording rules.

Boundary: this collection's board owns the requirements list and the decisions list. The installed skills still own a product repository's roadmap, decisions, and ADRs.

Pattern: `docs/REQUIREMENTS.md` is the list of statements. `docs/DECISIONS.md` is the one list of Open and Decided rows. `make toon` and `make project-report` read the requirements list when `docs/adr/` has no ADR file, and they still write the ADR index for a product repository.

## Develop

`docs/ROADMAP.md` and `docs/adr/` are gone. Open work is an Open row in `docs/DECISIONS.md`. Each still-true ADR rule is one statement in `docs/REQUIREMENTS.md`. The contract tests name those requirement ids. Python is the language skill for the index, the id check, and the report. Shell is the language skill for the Make include that exposes `toon` in this collection.

## Review

`make` with no target prints help. `make editorconfig`, `make format`, `make lint`, `make test`, `make integration`, `make coverage`, `make project-report`, `make test-changed`, `make ids`, and `make toon` passed. `make toon` wrote `docs/requirements-index.toon` and did not create `docs/adr/`.

security: the scripts read this repository. No listener, no secret, no personal data in a fixture.

privacy: no personal data.

ux-ui-design: no screen.

api-design: not HTTP. Not a module export. The interface is the Make targets. The scripts stay internal.

No finding. Left alone: a product repository that has an ADR file still gets `docs/adr/index.toon` and the product report. When that repository also has `docs/REQUIREMENTS.md`, the ADR index wins. The open histories stay open. This branch does not stack on the history-closing pull request.

## Release

Not invoked: this slice does not ship.
