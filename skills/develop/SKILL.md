---
name: develop
description: Implement a slice plan already closed, or a request that names a file or a failing test. Read the accepted ADRs before editing. Use the installed language skill for the files in hand. Two languages means two disjoint file sets. Stop when that language skill is not installed. Do not report done until make lint and make test have passed. Tests come with the behaviour change. Invoke record for ids and the Develop section.
---

# Develop

## Steps

1. If `docs/BUGS.md`, `docs/WAVES.md`, `docs/FEATURES.md`, `docs/bugs/`, `docs/waves/`, or `docs/features/` exists, stop. Name `migrate-docs`. Do not take a later step.
2. Invoke `record` before creating an id or a document. A write that skips `record` fails this step.
3. Do the work below, in order.
4. Ask `record` to write the Develop section, or one sentence that says why `develop` was not invoked. `record` rejects a history file missing Plan, Develop, Review, or Release.

## Work

1. Read the history file for this task. When there is none, because the request named a file or a failing test, ask `record` for a history id. The Plan section is then one sentence that says why `plan` was not invoked. When the slice starts from a proposal, the Plan section cites that proposal id. Do not copy the proposal into Develop.
2. Run `make toon`. Read `docs/skill-index.toon`. Invoke each `language` row whose `files` or `names` match the files in hand. A file set with no matching row stops this step.
3. Read `docs/adr/index.toon`. Open each ADR whose status is `Accepted` and whose `skills` names a skill this slice uses. Stop when the change would break an accepted ADR. Do not take a later step. Skip this step when the repository does not keep `docs/adr/`.
4. Two languages means two disjoint file sets. Finish one set before editing the other.
5. A behaviour change has a unit test. `make test` runs the unit tests. `make integration` is the one integration entry. Stop when one target runs both. Do not take a later step. Podman, XDG paths, and what a shipment may contain are `project-setup`. Do not restate them.
6. A test names the requirement it proves. The line is `id:` in the test's header or metadata, the line `record` matches. The id is a roadmap id, a known-issue id, an ADR id, or a decision id. When the repository keeps `docs/REQUIREMENTS.md` and does not keep `docs/adr/`, the id is a row in that list. The test name states what the system does when that requirement holds. Stop when a test has no id. Do not take a later step. Do not put the id in a path.
7. `make test` is the full suite. `make test-changed` runs the tests that cover the files in the diff. The selection is the coverage of those files. Stop when the selection is a hand-kept list, or when the coverage map is missing. Do not take a later step. Run `make coverage` to write the map, then `make test-changed`. A green `test-changed` does not replace `make test`.
8. A method does one thing, or it only composes other methods. Stop when a method does both. Do not take a later step.
9. Name a unit, a function, a method, a class, and a file from the domain. Stop when a name is not from the domain. Do not take a later step.
10. No skipped test. No silent catch. No secret and no personal data in a fixture. Stop when one of these is present. Do not take a later step.
11. Run `make lint` and `make test`. The linter is the one the language skill names. Do not write a linter. Stop when either target fails. Do not take a later step.
12. Run `make coverage`. It writes `build/coverage/diff.md` for the lines this change touched. Stop when that report is missing. Do not take a later step.
13. CI runs these same Make targets. `test-changed` is not a CI target. Stop when lint, test, or coverage runs outside Make. Do not take a later step.
14. An id, a roadmap line, or a known-issue change goes through `record`.
