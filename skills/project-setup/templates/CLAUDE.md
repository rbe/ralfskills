# [project name]

[One sentence that says what this project is.]

`CLAUDE.md` is the only entry file. The skills are installed under `.claude/skills/` with APM.

Stages, in order: `plan`, `develop`, `review`, `release`. A new or vague request starts at `plan`. A request that names a source file, a failing test, or a known issue starts at `develop`. `record` writes every id and every board document. `project-report` generates the requirements-to-tests map and the architecture and development reviews. `project-setup` is the Make contract. [Keep this sentence only when `github-pipeline` is installed:] `github-pipeline` is the delivery contract, and `release` invokes it when delivery changes.

Language skills: [the installed ones of `node`, `python`, `shell`, `jvm`, `go`]. Subskills `plan` asks and `review` checks: [the installed ones of `security`, `privacy`, `ux-ui-design`, `api-design`]. A project skill is an extra name listed here. [Name each project skill and each framework here, or write that there is none.]

`plan` names who owns state and what may call what. `develop` is not done until `make lint` and `make test` pass. The linter is the one the language skill names. `make test` is the full suite. `make test-changed` runs the tests that cover the diff. `make coverage` lists the lines the change touched. `make project-report` writes the generated report. `make format-fix` rewrites the files with the formatter.

This project ships [as a container image, with the merge into the default branch / as a binary, with `make <target>` / as a library package, with `make build` / as a library, with the merge into the default branch].

In-progress work is a line in `docs/ROADMAP.md`. A defect is a row in `docs/KNOWN_ISSUES.md`. A small choice is a row in `docs/DECISIONS.md`. An architecture or development rule is an ADR in `docs/adr/`. Work for later is a file in `docs/proposals/`. A started slice is a file in `docs/history/`. An accepted ADR is a rule for every change. A test names the ADR or the decision it proves with `id:`. Run `make toon` before reading an index. `make decision-log` writes the decisions as one document.

If `docs/BUGS.md`, `docs/WAVES.md`, `docs/FEATURES.md`, `docs/bugs/`, `docs/waves/`, or `docs/features/` exists, the only skill is `migrate-docs`.

The communication contract uses the names and concepts already in the project. Do not invent a synonym for a term the project already uses. The first sentence to the user states the understood intent, in one sentence. Stop when that sentence is wrong.

One idea per sentence. Be clear and on the point. English follows ASD-STE100. German follows "Deutsch für die Technische Kommunikation" (tekom Deutschland e.V.). Name the standards. Do not copy their text. Keep German and English separate.
