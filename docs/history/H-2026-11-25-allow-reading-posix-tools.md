---
id: H-2026-11-25-allow-reading-posix-tools
title: An agent may type a POSIX sh tool that only reads
status: closed
adrs: [R-75, R-76]
skills: [develop, review, record]
roadmap: []
proposals: []
---

# An agent may type a POSIX sh tool that only reads

## Plan

The owner merged PR 30 and chose that the rule "Type only `make <target>` and Git commands" also allows a typed tool of POSIX `sh` that only reads. `plan` was not invoked.

## Develop

The first bullet of Interface in the `<general_rules>` block of `CLAUDE.md` and of `skills/project-setup/templates/CLAUDE.md` now has the sentence "A typed tool of POSIX `sh`, such as `tail` or `grep`, may only shorten or search output, and writes no file." The two blocks are identical.

[R-75](../requirements/project-setup.md#r-75) owns the typed-command rule. It has one new sentence for the tools that only shorten or search output. No new id was issued. [R-76](../requirements/project-setup.md#r-76) states the word limits as 845 for `CLAUDE.md` and 915 for the template. Before, they were 824 and 894. The sentence has 21 words. `README.md` has the same sentence after "type only `make <target>` and Git commands".

`test_the_general_rules_name_the_interface_and_the_start_of_a_task` in `skills/project-report/scripts/test_project_report.py` proves the new sentence for both files. The word-limit test has the new limits. No existing test asserted the old sentence in a way that the new sentence breaks. `CLAUDE.md` has 844 words and the template has 915 words, read with `wc -w`.

Places that held text about the rule: `README.md` line 82 was changed. `skills/project-setup/references/fail-list.md`, `skills/project-setup/templates/contract-report.md`, and [R-89](../requirements/project-setup.md#r-89) speak of a recipe on the host, not of a typed command, so they stay.

## Review

`make toon`, `make links`, `make ids`, `make links-check`, `make editorconfig`, `make format`, `make lint`, and `make test` passed after the last edit. `make test` ran 136 tests.

security: the sentence allows only a tool that writes no file. No listener, no secret.

privacy, ux-ui-design, api-design: not touched.

Not run: `make integration` and `make coverage`.

## Release

Not invoked: the owner pushes this slice.
