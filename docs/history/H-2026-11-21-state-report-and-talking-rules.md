---
id: H-2026-11-21-state-report-and-talking-rules
title: The skill system-state-report and the talking rules of the owner
status: closed
adrs: []
skills: [develop, review, record, project-setup, system-state-report]
decisions: [D-14]
proposals: []
issues: []
---

# The skill system-state-report and the talking rules of the owner

## Plan

`plan` was not invoked. The owner named both parts and the place of the rules: the skill goes into this collection, and the rules go where every agent always reads them.

Boundary: `CLAUDE.md` is the only file that every agent reads in every session. The entry-file template of `project-setup` gives a product repository the same text. `record` owns the decision rows.

Pattern: one contract in `CLAUDE.md`. The skill refers to it and adds only what the contract lacks.

## Develop

The skill is copied from the skill `system-state-report` that the owner keeps outside this repository. The text of the skill changed in six places:

- The frontmatter has no quotes, like the other skills.
- Step 1 reads the board of this collection: `docs/DECISIONS.md`, `docs/KNOWN_ISSUES.md`, `docs/REQUIREMENTS.md`, `docs/adr/`, and `docs/history/`. It reads the output of `make project-report`, and it runs the tests through Make.
- Step 5 and the last section send a decision that has no row to `record`. The original wrote a `DECISIONS.md` in the project root and told the owner to add a rule to `CLAUDE.md` or `AGENTS.md`. This collection has `docs/DECISIONS.md`, and `CLAUDE.md` is the only entry file.
- The section `Language rules` is now `Rules of a report`. [R-51](../REQUIREMENTS.md#r-51) says that no `SKILL.md` restates the contract. The section keeps six rules that the contract lacks, such as the limit of 20 words for an instruction.
- Step 4 checks against the contract and the rules of a report.
- The purpose section says that the contract in `CLAUDE.md` applies to the report.

The communication contract in `CLAUDE.md` and in `skills/project-setup/templates/CLAUDE.md` is the text of the owner's talking rules. It replaces two shorter paragraphs. The first-sentence rule and the two standards stayed. The text now has a heading and four parts: names, sentences, content, and scope. D-14 records the choice. [R-51](../REQUIREMENTS.md#r-51) and [R-74](../REQUIREMENTS.md#r-74) state the contract and the skill.

`CLAUDE.md` and the template name the skill. The README has a row and a line in the `apm.yml` example.

## Review

Every gate passed through Make in Podman: `make links`, `make format`, `make lint`, `make test`, `make integration`, `make editorconfig`, `make coverage`, `make test-changed`, `make ids`, `make toon`, `make links-check`, `make project-report`, and `make decision-log`.

security: no code, no secret. privacy: no personal data. ux-ui-design, api-design: not touched.

Left alone: nobody ran the skill. The rules in `CLAUDE.md` were not tried by a second agent. `CLAUDE.md` of `gh-sweep` still has the old contract, because the owner did not ask for it.

## Release

The branch is committed. The merge into the default branch waits for the owner.
