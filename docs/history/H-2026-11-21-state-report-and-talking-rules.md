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

`plan` was not invoked. The owner asked for the skill in this collection and the rules where every agent reads them. `CLAUDE.md` is the one file that every session reads.

## Develop

The skill `system-state-report` was copied and changed in six places. The communication contract replaces two shorter paragraphs, and D-14 records that choice. [R-51](../requirements/collection.md#r-51) says no `SKILL.md` restates the contract. [R-74](../requirements/system-state-report.md#r-74) states the skill.

## Review

Gates passed in Podman, including `make links`, `make lint`, `make test`, and `make project-report`. Security, privacy, interaction, and API checks found nothing. Nobody ran the skill, and no second agent tested the rules.

## Release

The branch is committed. This slice does not merge it.
