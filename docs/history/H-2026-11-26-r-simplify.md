---
id: H-2026-11-26-r-simplify
title: One rules file, short pipeline rules and rows, a change diff that stages nothing
status: closed
adrs: [R-76, R-60, R-51, R-18, R-28, R-97, R-12]
skills: [r-project-setup, r-github-pipeline, r-record, r-onboard, r-skills-review, r-node, r-python, r-go, r-jvm]
roadmap: []
proposals: []
---

# One rules file, short pipeline rules and rows, a change diff that stages nothing

## Plan

The owner chose items 1, 2, 3 and the coverage defect of the simplification review of 2026-11-26. `r-plan` was not invoked.

## Develop

`skills/r-project-setup/rules.md` holds the general rules, the Agents section, and the communication contract. `CLAUDE.md` and its template import it with one `@` line. The pipeline-rules template keeps one paragraph, "This repository", and "Divergences". `CHANGE_DIFF` and `DIFF_BASE` in `tools.mk` write `build/coverage/change.diff`; no template runs `git add -N .`. The requirement rows went from 19,564 to 9,586 words. A Sonnet agent shortened the rows. The orchestrator re-read a sample and re-ran the gates.

## Review

`make editorconfig`, `format`, `lint`, `test` (201 tests), `integration`, and `coverage` (100% of the changed lines) passed. The new `@` import was checked: this session loaded `rules.md` through it.

## Release

The owner merges the pull request and tags v0.7.0.
