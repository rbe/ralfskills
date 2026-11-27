---
id: H-2026-11-25-test-repository-method
title: The test in a test repository is documented
status: closed
adrs: [R-100]
skills: [develop, review, record]
roadmap: []
proposals: []
---

# The test in a test repository is documented

## Plan

The owner merged PR 29, removed the two test branches of `rbe/gh-sweep`, and asked to document how to use them again. `plan` was not invoked. Its limits: never push to `main`, never delete a release, tag, or package version.

## Develop

The README section "Test the collection in a test repository" has five numbered steps. [R-100](../requirements/collection.md#r-100) states the rule. One test pins the heading, the branch names, and the limits.

## Review

Gates passed after the last edit: `make toon`, `make links`, `make ids`, `make links-check`, `make editorconfig`, `make format`, `make lint`, and `make test`. Security: the README names the one real deletion, the Actions artifacts. Not run: `make integration`, `make coverage`, and the README steps on GitHub.

## Release

Not invoked: the owner pushes this slice.
