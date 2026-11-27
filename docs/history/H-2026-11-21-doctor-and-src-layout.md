---
id: H-2026-11-21-doctor-and-src-layout
title: make doctor, the src layout, and the owner from the remote
status: closed
adrs: []
skills: [develop, review, record, project-setup, github-pipeline, python, onboard, shell]
decisions: []
proposals: []
issues: []
---

# make doctor, the src layout, and the owner from the remote

## Plan

`plan` was not invoked. The owner asked for item 5 of the trial review: prerequisites are checked, and a `src/` layout works. `project-setup` owns `doctor.mk`.

## Develop

`doctor.mk` has `make doctor`. It checks Make, Git, and `podman info`, and with a workflow it checks `origin` and `gh`. [R-73](../requirements/project-setup.md#r-73) states it. `make setup` runs `make doctor` first. `cover_tests.py` puts `src/` on the Python path.

## Review

Gates passed in Podman, including `make coverage`, `make test-changed`, and `make toon`. `make doctor` printed `ok` here, and printed `FAIL` with no Podman on `PATH`. Security: `doctor` changes nothing and prints no secret. No finding.

## Release

The branch is committed. This slice does not merge it.
