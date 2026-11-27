---
id: H-2026-11-20-trial-findings
title: Fix what two trial projects found
status: closed
adrs: []
skills: [plan, develop, review, release, record, project-report, project-setup, github-pipeline, node, python, shell, security, migrate-docs]
decisions: [D-9]
proposals: []
issues: []
---

# Fix what two trial projects found

## Plan

`plan` was not invoked. Two agents set up a Node project and onboarded a Python project with an old board. Their findings are the input.

## Develop

A test names an ADR or a decision, not a roadmap line. D-9 records that choice. `python` and `node` have Makefile templates, and `$(NODE)` runs Node in Podman. `make format` checks, and `make format-fix` rewrites. Python and shell are the language skills.

## Review

Gates passed in Podman. Two more agents repeated both trials, and all twelve Make targets passed in each project. Their remaining findings are fixed here too. Security, privacy, interaction, and API checks found nothing.

## Release

The branch is pushed and merged into the default branch with a pull request, after the owner confirmed. This collection publishes no image.
