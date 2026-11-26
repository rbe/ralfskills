---
id: H-2026-11-26-one-owner-each-rule
title: Give each rule one owner
status: closed
adrs: [R-51, R-74, R-31, R-32, R-37, R-40]
skills: [r-record, r-skills-review, r-system-state-report]
roadmap: []
proposals: []
---

# Give each rule one owner

## Plan

The owner chose one owner for each rule and no new duplicate test. The input was a list of 20 candidates. `r-plan` was not invoked.

## Develop

Fixed audit candidates 1, 2, 3, 6, 7, 10, 12, 13, 14, 15, and 20 in 14 skill files and 4 requirement rows. [R-74](../requirements/system-state-report.md#r-74) no longer restates the contract. Rejected 4, 5, 8, 9, 11, 16, 17, 18, and 19, each as an action, an own fact, or an owner question. No test changed.

## Review

`make editorconfig`, `format`, `lint`, `test` (145 tests), and `coverage` (100%) passed. `make integration` is `true`. Word limits stay 847 and 917.

## Release

Not invoked: this slice does not ship.
