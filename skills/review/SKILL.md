---
name: review
description: Check a change after implementation and before it ships. Run the gates and each check row in docs/skill-index.toon. A missing line for a row fails the check. Write findings through record. Do not weaken a test.
---

# Review

## Steps

1. If `docs/BUGS.md`, `docs/WAVES.md`, `docs/FEATURES.md`, `docs/bugs/`, `docs/waves/`, or `docs/features/` exists, stop. Name `migrate-docs`. Do not take a later step.
2. Invoke `record` before creating an id or a document. A write that skips `record` fails this step.
3. Do the work below, in order.
4. Ask `record` to write the Review section, or one sentence that says why `review` was not invoked. `record` rejects a history file missing Plan, Develop, Review, or Release.

## Work

1. Run `make toon`. Read `docs/skill-index.toon`. For each row whose `kind` is `check`, in file order, read that skill and run its checks. If there is no `check` row, write `checks: none installed`. A missing line for a row fails this step.
2. Run `make test` for the change. A gate that did not run is reported as not run, with the reason. Do not weaken a test to make the change pass.
3. A finding has a location, the mechanism, the evidence, whether it predates this change, and the check that proves the fix. A model or prompt change needs a baseline from the same session.
4. A finding that is fixed stays in this change. A finding that waits becomes a known-issue id through `record`.
5. Write what this change deliberately left alone.
