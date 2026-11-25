---
id: H-2026-11-25-readme-migration-facts
title: The README states three facts for the migration of a project
status: closed
adrs: [R-72]
skills: [develop, review, record]
roadmap: []
proposals: []
---

# The README states three facts for the migration of a project

## Plan

The owner migrates existing projects onto the collection and asked to add three facts to the README. `plan` was not invoked. The owner also said "update the diagrams". The repository holds no diagram, so no diagram changed.

## Develop

The README states three facts. In a project with an old board, `make old-board` fails first, as designed, and the only skill is then `migrate-docs`. This extends the sentence in step 3 of the `onboard` list. `make skills-update` can refuse when `.claude/skills/` holds files that APM did not install, which APM calls unmanaged. `make apm ARGS='install --force'` then overwrites them with the files of the collection. This sits in the Update section, and the section "Test the collection in a test repository" now points to it. A project whose documents hold ids above the counters of `docs/ids.yaml` fails `make ids`, and `make id-raise KIND=<kind> TO=<n>` raises the counter. This is a new paragraph at the end of the Update section.

[R-72](../requirements/collection.md#r-72) has one new sentence that says the README states these facts. One new test in `skills/project-report/scripts/test_project_report.py` names `id: R-72` and pins the three facts by their target names.

Facts read in the code: `skills/project-setup/old-board.mk` fails and prints that the only skill is `migrate-docs`. `skills/project-setup/skills.mk` defines `apm`, which runs `$(APM) $(ARGS)`. `skills/record/scripts/ids.py` reports an id above its counter, and its `raise` command sets a counter only to a higher number. `skills/migrate-docs/SKILL.md` step 3 names `make id-raise KIND=<kind> TO=<highest number used>`. The refusal for unmanaged files is a behaviour of APM 0.36.1. The earlier test-repository slice recorded it, and no code of this collection shows it.

## Review

After the last edit, `make toon`, `make links`, `make ids`, `make links-check`, `make editorconfig`, `make format`, `make lint`, and `make test` passed. `make test` ran 137 tests.

security, privacy, ux-ui-design, api-design: not touched.

Not run: `make integration` and `make coverage`.

## Release

Not invoked: the owner pushes this slice.
