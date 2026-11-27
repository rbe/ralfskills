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

The owner asked to add the diagrams "ralfskills Map" and "ralfskills Board Map" to the repository and show them in the README. Before, they were web pages outside the repository. `plan` was not invoked.

## Develop

`docs/diagrams/collection-map.svg` and `docs/diagrams/board-map.svg` hold the two diagrams, each with its own styles for light and dark pages. The README has the sections "How the parts work together" and "The cycle", with seven and six steps. [R-101](../requirements/collection.md#r-101) is the new rule, and one test names it.

## Review

Gates passed after the last edit, including `make test` with 138 tests and `make coverage`, which reported 14 changed lines, all covered. Both SVG files were checked in Chromium, in light and dark mode. Security, privacy, interaction, and API checks were not touched.

## Release

Not invoked: the owner merges the pull request.
