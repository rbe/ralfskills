---
id: H-2026-11-26-component-upgrade-skills
title: The collection adds component-upgrade and one upgrade skill per language
status: closed
adrs: [R-104, R-76]
skills: [develop, review, record]
roadmap: []
proposals: []
---

# The collection adds component-upgrade and one upgrade skill per language

## Plan

On 2026-11-26 the owner chose a skill `component-upgrade` for all component updates, so that one skill owns every update. The owner then chose the split "component-upgrade plus one per language": `component-upgrade` holds the shared steps once. `upgrade-node-components`, `upgrade-python-components`, `upgrade-java-components`, and `upgrade-go-components` hold only the facts of one environment. `plan` was not invoked.

## Develop

[R-104](../requirements/component-upgrade.md#r-104) is the rule for the five skills. `component-upgrade` updates one component in one slice. It points to the Update section of the README for this skill collection, and it keeps a gate baseline from before the change. Step 4 points to the skill `upgrade-<language>-components` that matches the component.

Each language skill lists the pins, the Make target that changes the lock file, and the traps. Each fact comes from the templates and the references of this repository. The collection names no target that writes a lock file for Python or for Gradle, so those skills say so. The collection names no pin for Grails or for `.nvmrc`, so the skills leave them out.

The skill lists in `CLAUDE.md`, in the `CLAUDE.md` template of `project-setup`, in [R-60](../requirements/project-setup.md#r-60), and in the skill table and the `apm.yml` sample of the README name the five skills.

Tests in `skills/project-report/scripts/test_project_report.py` name `id: R-104`.

## Review

After the last edit, `make toon`, `make links`, `make ids`, `make links-check`, `make format-fix`, `make editorconfig`, `make format`, `make lint`, `make test`, `make integration`, and `make coverage` passed. `make test` ran 142 tests. `make coverage` reports 47 changed lines, all covered. The gates ran in a cloud container with Docker behind a `podman` shim.

security, privacy, ux-ui-design, api-design, observability, performance: not touched.

The skill count is now 29. `CLAUDE.md` and its template went 2 words over the limits of [R-76](../requirements/project-setup.md#r-76). The list now reads `component-upgrade`/`upgrade-<language>-components`, one word. The limits did not change, at 847 and 917.

