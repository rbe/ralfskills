---
name: review
description: Check a change after implementation and before it ships. Run the gates and each check row in docs/skill-index.toon. A change that breaks an accepted ADR is a finding. A missing line for a row fails the check. A method, a domain name, or the pattern plan named can fail the check. Write findings through record. Do not weaken a test.
---

# Review

## Steps

1. If `docs/BUGS.md`, `docs/WAVES.md`, `docs/FEATURES.md`, `docs/bugs/`, `docs/waves/`, or `docs/features/` exists, stop. Name `migrate-docs`. Do not take a later step.
2. Invoke `record` before creating an id or a document. A write that skips `record` fails this step.
3. Do the work below, in order.
4. Ask `record` to write the Review section, or one sentence that says why `review` was not invoked. `record` rejects a history file missing Plan, Develop, Review, or Release.

## Work

1. Run `make toon`. Read `docs/skill-index.toon`. For each row whose `kind` is `check`, in file order, read that skill and run its checks. If there is no `check` row, write `checks: none installed`. A missing line for a row fails this step. A check that does not apply to this change is one line that says why.
2. Read `docs/adr/index.toon`. Open each ADR whose status is `Accepted` and whose `skills` names a skill this slice uses. A change that breaks an accepted ADR is a finding. An accepted ADR replaces a skill rule only when the ADR is a divergence. A divergence names the rule, what differs, and why. An ADR that differs from a skill rule and does not name these three is a finding. What `github-pipeline` says is not a divergence stays not allowed. Skip this step when the repository does not keep `docs/adr/`.
3. Run `make lint` and `make test` for the change. A gate that did not run is reported as not run, with the reason. Do not weaken a test to make the change pass. Do not skip a test. `make test` is the full suite. A green `test-changed` does not replace `make test`.
4. A test names the requirement it proves. The line is `id:` in the test's header or metadata, the line `record` matches. The id is an ADR id or a decision id. A roadmap line and a known issue are work, not rules. Their ids are retired when the work ends, so a test does not name them. A test for a fixed known issue names the ADR or the Decided entry that states the fixed behaviour. `record` writes that Decided entry when there is none. When the repository keeps `docs/REQUIREMENTS.md` and does not keep `docs/adr/`, the id is a row in that list. The test name states what the system does when that requirement holds. Stop when a test has no id. Do not take a later step. An id in a path fails this check.
5. Run `make project-report`. It writes `build/project-report.md`: the requirements-to-tests map, the architecture review, and the development review. Stop when the target fails, when a part is missing, or when the file was hand-edited. Do not take a later step. Hand-editing it is a defect.
6. A finding has a location, the mechanism, the evidence, whether it predates this change, and the check that proves the fix. A model or prompt change needs a baseline from the same session.
7. A finding that is fixed stays in this change. A finding that waits becomes a known-issue id through `record`.
8. Write what this change deliberately left alone.
9. Read `build/coverage/diff.md`. It lists the lines this change touched. A repository-wide percentage used as the result is a finding. A missing report is not run, with the reason.
10. These are findings, in one check: a method that neither does one thing nor only composes other methods; a unit, function, method, class, or file whose name is not from the domain; code that ignores the pattern Plan named. Plan chose the pattern. Do not name a different pattern.
11. A skipped test, a silent catch, or a secret or personal data in a fixture is a finding.
12. CI runs `make editorconfig`, `make format`, `make lint`, `make test`, `make integration`, and `make coverage`. `test-changed` is not a CI target. A step that is not `make <target>` is a finding.
