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

1. Run `make toon`. Read `docs/ROADMAP.md`, `docs/KNOWN_ISSUES.md`, `docs/DECISIONS.md`, `docs/adr/index.toon`, `docs/skill-index.toon`, and the open files in `docs/proposals/`. A file that does not exist yet has nothing to read. `record` creates it from its template at the first write. When the repository keeps `docs/REQUIREMENTS.md` and does not keep `docs/adr/`, read that list and `docs/DECISIONS.md` instead of `docs/ROADMAP.md` and `docs/adr/index.toon`. Read an ADR when the index names an id this slice can change. Follow only an ADR whose status is `Accepted`. Do not ask a question an accepted ADR, a Decided entry, or an open proposal already answered. A proposal with no answers gets the whole grill now. The answers go into the Plan section of the history file, and the proposal keeps its text.
2. For each `skill-index` row whose `kind` is `check`, in file order: read that skill and ask its questions. When the request is too vague for these questions, do step 3 first and ask them when the slice is one sentence. Answer a question from the code or the board when they answer it, and write that answer down. If there is no `check` row, write `checks: none installed`. A missing line for a row fails this step. No history file is open yet. Keep the answers, and write one line for each row in the Plan section when the file exists.
3. Ask one question, then wait. Before the slice closes, ask what the result looks like: the output or the interface, the empty case, and the error case. `develop` cannot ask the owner later. Stop when the slice is one sentence, with an out-of-scope line. A request that already names a source file, a failing test, or a known issue is `develop`.
4. Name the boundary and the pattern for this slice: who owns state, and what may call what. When the boundary keeps the slice out of a package, name each existing function in that package that the slice needs, and say whether the slice moves it, exports it, or repeats it. Architectural patterns are part of the grill in step 3. Stop when that sentence is missing. Do not take a later step.
5. Evaluate architecture, scalability, and code quality against the constraints of this system. Prefer the smallest design that stays operable and maintainable. When a choice is expensive to reverse, name the options, recommend one, and wait. Otherwise implement it in small modules.
6. When the owner answers a choice that is expensive to reverse, ask `record` for an ADR id. A storage format, a protocol, and the interface of a library that other code imports are such choices. The interface is the public names and their signatures, and it is the ADR. What a function does is Decided rows. `record` writes `docs/adr/<id>.md` with the status `Accepted`. The Plan section cites that id. A choice that is cheap to reverse stays a Decided entry. When the repository keeps `docs/REQUIREMENTS.md` and does not keep `docs/adr/`, the answer is a row in that list.
7. Invoke `project-setup` when the Makefile is missing, or when the slice adds or overrides a target. Do not invoke it otherwise.
8. Stop when the slice needs a language and no `language` row in `docs/skill-index.toon` matches the files. A row is installed: the index lists only installed skills.
9. Implement now: create the branch of the slice. Ask `record` for a history id. `record` writes the file from its template and adds one roadmap line with that id. Write the questions and answers in Plan, including the boundary and the pattern. Each answer that a test must prove becomes a Decided row through `record`, or an ADR as step 6 says. `develop` names those ids in the tests. Develop, Review, and Release are `Not invoked yet.` Do not copy the grill into the roadmap.
10. Implement later: ask `record` for a proposal id and write `docs/proposals/<id>.md`. That file is the backlog. Do not create a history file. Do not add a roadmap line.
