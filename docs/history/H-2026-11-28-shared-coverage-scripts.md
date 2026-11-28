---
id: H-2026-11-28-shared-coverage-scripts
title: The pytest and JaCoCo coverage scripts of three projects move into r-project-report
status: closed
adrs: []
skills: [r-record, r-develop, r-review]
roadmap: []
proposals: []
---

# The pytest and JaCoCo coverage scripts of three projects move into r-project-report

## Plan

`r-plan` was not invoked. The owner approved the verdicts of the script and skill review on 28 November 2026.

## Develop

`r-project-report` has three new scripts. `pytest_cover.py` comes from emailtodisk and runs pytest for `make coverage` and `make test-changed` ([R-155](../requirements/python.md#r-155)). `jacoco_repo_paths.py` comes from odisee26 ([R-156](../requirements/jvm.md#r-156)). `jacoco_summary.py` comes from erechnung ([R-157](../requirements/jvm.md#r-157)). `references/makefile.md` of `r-python` and `references/gradle.md` of `r-jvm` say when to use them. The client tag check needed no new script: `templates/publish-client.yml` of `r-github-pipeline` already has it. R-158 was issued and not used.

## Review

`TOOLS=host make gates` ran in the cloud session. The pull request states the result.

## Release

Ships with the merge of the pull request by the owner and the next tag.
