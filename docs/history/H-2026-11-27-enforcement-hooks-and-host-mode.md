---
id: H-2026-11-27-enforcement-hooks-and-host-mode
title: The pre-push hook checks the pushed commit, a board check in make test, a bypass guard, and host mode
status: open
adrs: [R-1, R-13, R-40, R-69, R-75, R-89, R-120, R-124, R-127, R-129, R-130]
skills: [plan, develop, review, record, python, shell]
roadmap: []
proposals: []
---

# The pre-push hook checks the pushed commit, a board check in make test, a bypass guard, and host mode

## Plan

A report-only review of the rule enforcement found four holes in the pre-push hook of [R-127](../requirements/project-setup.md#r-127). The hook compared the files on disk, not the pushed commit. It refused the close commit of `r-release`. Only `make setup` installed it. `--no-verify` skipped it. The owner chose all four proposals P1 to P4. The owner also chose host mode, `TOOLS=host`, so a cloud session without Podman runs every gate through Make. Declined: a host-tool blocker, because a cloud session cannot run Podman. Declined: a `SessionStart` hook, because `make gates` installs the git hook for any agent. The owner moved the secret scanner to a later security session.

## Develop

P1: `pre-push.sh` reads the pushed refs from stdin, compares the tree of each pushed commit with `build/gates.ok`, and accepts a difference in `BOARD_FILES` only. For a `v*` tag it runs `make check-tag` with `PUSHED`. P2: `gates` and `test-changed` depend on `git-hooks`. P3: `make board-check` runs `ids`, `links-check`, and `test-ids`, and `make test` runs it. P4: `block-hook-bypass.sh` refuses `--no-verify` and `core.hooksPath`. Host mode: `TOOLS=host` in `podman-python.mk`, `tools.mk`, `node.mk`, `go.mk`, `jvm.mk`, and `sdlc.mk`, and the target `host-tools`. The orchestrator wrote all changes without a subagent.

## Review

`TOOLS=host make gates` passed in a cloud session without Podman: editorconfig, format, lint, test (268 tests), integration, and coverage. `make board-check` passed on the 7 product clones with the new scripts. Not run: the gates in Podman mode, because this machine has no Podman; `make host-tools` with apm and Gradle in host mode on a JVM project.

## Release
