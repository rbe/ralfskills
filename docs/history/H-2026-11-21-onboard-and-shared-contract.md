---
id: H-2026-11-21-onboard-and-shared-contract
title: One onboard skill, one shared contract, and a delivery that fits every language
status: closed
adrs: []
skills: [plan, develop, review, record, project-setup, github-pipeline, onboard, shell]
decisions: [D-13]
proposals: []
issues: []
---

# One onboard skill, one shared contract, and a delivery that fits every language

## Plan

The owner asked whether a project can start with the APM skills and `report and integrate`. The review found three blockers. `onboard` owns only the order of the other skills.

## Develop

`contract.mk` in `project-setup` holds the contract targets. [R-71](../requirements/project-setup.md#r-71) states it. `sdlc.mk` includes `contract.mk` and `container.mk`. [R-70](../requirements/onboard.md#r-70) states the skill `onboard`, which has ten steps.

## Review

Gates passed in Podman, including `make toon`, `make links-check`, and `make project-report`. Security: the workflow keeps the same permissions. No finding. No fresh agent ran `report and integrate` with `onboard` yet.

## Release

Committed on the working branch. This slice does not merge it.
