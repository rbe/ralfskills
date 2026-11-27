---
id: H-2026-11-20-apm-install
title: Make the collection install with APM and select changed tests in Node and the JVM
status: closed
adrs: []
skills: [develop, review, record, project-report, project-setup, github-pipeline, node, jvm, python, shell]
decisions: []
proposals: []
issues: []
---

# Make the collection install with APM and select changed tests in Node and the JVM

## Plan

`plan` was not invoked. The gaps were: APM install was untested, Node and JVM projects had no changed-test selection, and no Containerfile template existed.

## Develop

APM 0.36.1 refused the collection, because four skill descriptions had a colon and a space. [R-65](../requirements/record.md#r-65) states the rule. Coverage map scripts for Node and JaCoCo feed `changed_tests.py`. The Node and Gradle templates set `TEST_CHANGED_CMD`. `github-pipeline` gained Containerfile and ignore-file templates.

## Review

Gates passed in Podman, including `make test`, `make lint`, `make format`, and `make test-changed`. diff-cover ran on the host. APM installed nine skills into a sample project. No finding.

## Release

The branch was pushed and merged into the default branch with a pull request, after the owner confirmed. This collection publishes no image.
