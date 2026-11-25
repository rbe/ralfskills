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

`plan` was not invoked. The owner asked for item 5 of the trial review: `make setup` and `make doctor` check the prerequisites, and a `src/` layout works. The owner's earlier list also had the owner of the image filled from the remote.

Boundary: `project-setup` owns `doctor.mk` and `podman-python.mk`. `project-report` owns `cover_tests.py`. `github-pipeline` owns `container.mk`.

Pattern: `doctor` is its own file that both entry makefiles include, because the Node and Gradle templates do not include `contract.mk`.

## Develop

`doctor.mk` has `make doctor`. It checks Make, Git, and `podman info`. When the project has a workflow it also checks the remote `origin` and `gh`. A missing `gh` is a warning. [R-73](../requirements/project-setup.md#r-73) states it.

`make setup` runs `make doctor` first in `contract.mk`, and in `_setup` of the Node and Gradle templates.

`$(PYTHON)` sets `PYTHONPATH=/work/src`. `cover_tests.py` puts `src/` on `sys.path` when the directory exists.

`OWNER` and `NAME` in `container.mk` default to the values in the URL of `origin`, in lower case for the owner. `Makefile.image` lost its two placeholders.

## Review

Every gate passed through Make in Podman: `make links`, `make format`, `make lint`, `make test`, `make integration`, `make editorconfig`, `make coverage`, `make test-changed`, `make ids`, `make toon`, `make links-check`, `make project-report`, and `make decision-log`.

Trial runs: a Python project with `src/invoicer` ran `make test`, `make coverage`, and `make test-changed`. The coverage report names `src/invoicer/__init__.py` and the lines of the change. `make doctor` printed `ok` on this machine. With a `PATH` that has no Podman it printed `FAIL` and exited 1, and `DOCTOR_SKIP_PODMAN=1` skipped the check. The owner default gave `ghcr.io/rbe/gh-sweep` for an HTTPS URL, `ghcr.io/some-owner/my.repo` for an SSH URL, and the directory name with no remote.

security: `doctor` reads versions and the remote URL. It changes nothing and prints no secret. `PYTHONPATH` holds one directory inside the project mount.

privacy: the remote URL stays on the machine.

ux-ui-design: the output of `doctor` is one line per check, with the fix on the next line.

api-design: not HTTP. `DOCTOR_SKIP_PODMAN`, `OWNER`, and `NAME` are the interface.

No finding. Left alone: no unit test covers `doctor.mk`, because the unit tests run in a container that has no Make and no Podman. The macOS branch of `doctor`, with a stopped Podman machine, did not run. A project that has `src/` and installs its package with `pip` was not tried.

## Release

The branch is committed. This slice does not merge it.
