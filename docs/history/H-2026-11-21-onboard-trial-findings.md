---
id: H-2026-11-21-onboard-trial-findings
title: Findings of the first agent trial of onboard
status: closed
adrs: []
skills: [develop, review, record, onboard, migrate-docs, project-setup, github-pipeline, python]
decisions: []
proposals: []
issues: []
---

# Findings of the first agent trial of onboard

## Plan

`plan` was not invoked. A fresh agent ran `report and integrate` on a Python project with an old board. It reported 13 findings, and eleven were skill defects.

## Develop

`migrate-docs` and `onboard` test the six old paths with `ls -d`, because Git does not list an empty directory. `python-tooling` writes `*.pyc` and `.ruff_cache/` to `.gitignore`. `onboard` step 10 reads tags with `git ls-remote --tags`.

## Review

Gates passed in Podman. The agent ran onboard through every step, and `make ci`, `make doctor`, and `make build` passed. Security: the new `.gitignore` lines keep generated files out of git. No finding.

## Release

Merged into the default branch with a pull request after the owner confirmed. The owner named `v0.1.0` as the first tag.
