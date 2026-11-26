---
id: H-2026-11-26-readme-diagrams
title: The README shows the two diagrams of the collection
status: closed
adrs: [R-101]
skills: [develop, review, record]
roadmap: []
proposals: []
---

# The README shows the two diagrams of the collection

## Plan

The owner asked to add the two diagrams "ralfskills Map" and "ralfskills Board Map" to the repository and to show them in the README with their explanations. Before, the two diagrams were web pages outside the repository. `plan` was not invoked.

## Develop

`docs/diagrams/collection-map.svg` and `docs/diagrams/board-map.svg` hold the SVG of the two pages. Each file has its own styles, a `<title>`, and colours for a light and a dark page, because GitHub shows an SVG in the README as an image without the styles of the page. The label `ci-status, pull-request, publish-container` now has three lines, because one line crossed the frame of the GitHub box.

The README has a new section "How the parts work together" with the first diagram, its explanation, and seven steps. The section "The cycle" shows the second diagram, its explanation, and six steps. Step 6 says what close mode does with the history file, the roadmap row, and the proposal, as `skills/record/references/close.md` says.

[R-101](../requirements/collection.md#r-101) is the new rule. One new test in `skills/project-report/scripts/test_project_report.py` names `id: R-101`.

## Review

After the last edit, `make toon`, `make links`, `make ids`, `make links-check`, `make editorconfig`, `make format`, `make lint`, `make test`, `make integration`, and `make coverage` passed. `make test` ran 138 tests. `make coverage` reports 14 changed lines, all covered. The gates ran in a cloud container with Docker behind a `podman` shim and local stand-ins for the Ruff and editorconfig-checker images.

Both SVG files were rendered as images in Chromium, in light and in dark mode, and checked by eye.

security, privacy, ux-ui-design, api-design: not touched.

## Release

Not invoked: the owner merges the pull request.
