---
id: H-2026-11-21-node-tooling
title: make node-tooling sets up the Node tooling in one run
status: closed
adrs: []
skills: [develop, review, record, project-setup, node, shell]
decisions: []
proposals: []
issues: []
---

# make node-tooling sets up the Node tooling in one run

## Plan

`plan` was not invoked. The owner gave the target text for the Node template.

## Develop

The Node template has the target `node-tooling`. It creates a missing `package.json`, adds dev tools at exact versions, writes missing config files, and runs `make format-fix`. [R-66](../requirements/collection.md#r-66) states it. Shell is the language skill.

## Review

Gates passed in Podman. A new directory ran the target, and a second run changed no file. Security: npm runs in Podman, and `package-lock.json` pins the tree. No finding.

## Release

The branch is pushed and merged into the default branch with a pull request, after the owner confirmed. This collection publishes no image.
