---
id: H-2026-11-25-allow-reading-posix-tools
title: An agent may type a POSIX sh tool that only reads
status: closed
adrs: [R-75, R-76]
skills: [develop, review, record]
roadmap: []
proposals: []
---

# An agent may type a POSIX sh tool that only reads

## Plan

The owner merged PR 30 and chose to let a typed POSIX `sh` tool that only reads count under the rule "Type only `make <target>` and Git commands." `plan` was not invoked.

## Develop

The Interface rule now names tools such as `tail` or `grep` that only shorten or search output and write no file. [R-75](../requirements/project-setup.md#r-75) owns the rule, and no id was issued. [R-76](../requirements/project-setup.md#r-76) raised the word limits to 845 and 915. [R-89](../requirements/project-setup.md#r-89) stays, because it speaks of a host recipe.

## Review

Gates passed in Podman after the last edit, including `make test` with 136 tests, `make toon`, and `make links-check`. Security: the sentence allows only a tool that writes no file. Not run: `make integration` and `make coverage`.

## Release

Not invoked: the owner pushes this slice.
