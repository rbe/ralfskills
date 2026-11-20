---
name: plan
description: Grill a change before editing. Use when a request is new, vague, or would change a decision, an ADR, the roadmap, or a proposal. Ask one question at a time. Name the boundary and the pattern before the slice is closed. A named source file, a failing test, or a known issue is develop. Invoke project-setup when the Makefile is missing or a target changes. Stop and name migrate-docs when the old board is still present.
---

# Plan

## Steps

1. If `docs/BUGS.md`, `docs/WAVES.md`, `docs/FEATURES.md`, `docs/bugs/`, `docs/waves/`, or `docs/features/` exists, stop. Name `migrate-docs`. Do not take a later step.
2. Invoke `record` before creating an id or a document. A write that skips `record` fails this step.
3. Do the work below, in order.
4. Ask `record` to write the Plan section, or one sentence that says why `plan` was not invoked. `record` rejects a history file missing Plan, Develop, Review, or Release.

## Work

1. Run `make toon`. Read `docs/ROADMAP.md`, `docs/KNOWN_ISSUES.md`, `docs/DECISIONS.md`, `docs/adr/index.toon`, `docs/skill-index.toon`, and the open files in `docs/proposals/`. A file that does not exist yet has nothing to read. `record` creates it from its template at the first write. When the repository keeps `docs/REQUIREMENTS.md` and does not keep `docs/adr/`, read that list and `docs/DECISIONS.md` instead of `docs/ROADMAP.md` and `docs/adr/index.toon`. Read an ADR when the index names an id this slice can change. Follow only an ADR whose status is `Accepted`. Do not ask a question an accepted ADR, a Decided entry, or an open proposal already answered.
2. For each `skill-index` row whose `kind` is `check`, in file order: read that skill and ask its questions. If there is no `check` row, write `checks: none installed`. A missing line for a row fails this step. No history file is open yet. Keep the answers, and write one line for each row in the Plan section when the file exists.
3. Ask one question, then wait. Stop when the slice is one sentence, with an out-of-scope line. A request that already names a source file, a failing test, or a known issue is `develop`.
4. Name the boundary and the pattern for this slice: who owns state, and what may call what. Architectural patterns are part of the grill in step 3. Stop when that sentence is missing. Do not take a later step.
5. Evaluate architecture, scalability, and code quality against the constraints of this system. Prefer the smallest design that stays operable and maintainable. When a choice is expensive to reverse, name the options, recommend one, and wait. Otherwise implement it in small modules.
6. When the owner answers a choice that is expensive to reverse, ask `record` for an ADR id. `record` writes `docs/adr/<id>.md` with the status `Accepted`. The Plan section cites that id. A choice that is cheap to reverse stays a Decided entry. When the repository keeps `docs/REQUIREMENTS.md` and does not keep `docs/adr/`, the answer is a row in that list.
7. Invoke `project-setup` when the Makefile is missing, or when the slice adds or overrides a target. Do not invoke it otherwise.
8. Stop when the slice needs a language and no `language` row in `docs/skill-index.toon` matches the files. A row is installed: the index lists only installed skills.
9. Implement now: create the branch of the slice. Ask `record` for a history id. `record` writes the file from its template and adds one roadmap line with that id. Write the questions and answers in Plan, including the boundary and the pattern. Develop, Review, and Release are `Not invoked yet.` Do not copy the grill into the roadmap.
10. Implement later: ask `record` for a proposal id and write `docs/proposals/<id>.md`. That file is the backlog. Do not create a history file. Do not add a roadmap line.
