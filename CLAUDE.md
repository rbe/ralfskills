# ralfskills

This repository is the skill collection. `CLAUDE.md` is the only entry file.

Stages, in order: `plan`, `develop`, `review`, `release`. `record` writes every id and every board document. `project-report` generates the requirements-to-tests map and the architecture and development reviews. `project-setup` is the Make contract. `github-pipeline` is the delivery contract, and `release` invokes it when delivery changes.

Language skills: `node`, `python`, `shell`, `jvm`, `go`. Subskills `plan` asks and `review` checks: `security`, `privacy`, `ux-ui-design`, `api-design`. A project skill is an extra name listed here.

`plan` names who owns state and what may call what. `develop` is not done until `make lint` and `make test` pass. The linter is the one the language skill names. `make test` is the full suite. `make test-changed` runs the tests that cover the diff. `make coverage` lists the lines the change touched. `make project-report` writes the generated report.

This collection records each requirement as one row in `docs/REQUIREMENTS.md`. An Open row in `docs/DECISIONS.md` is work that is not finished. A Decided row is a choice in force. This collection does not keep `docs/ROADMAP.md` or `docs/adr/`. The skills still teach a product repository to keep in-progress work in `docs/ROADMAP.md`, choices in `docs/DECISIONS.md`, and a rule in `docs/adr/`. `make toon` writes `docs/requirements-index.toon` and `docs/skill-index.toon` here. In a product repository it writes `docs/adr/index.toon` and the skill index. Run `make toon` before reading an index. `make decision-log` writes `build/decision-log.md`, the decisions as one document. An id in a document under `docs/` is a link. `make links` writes the links, and `make links-check` checks them.

If `docs/BUGS.md`, `docs/WAVES.md`, `docs/FEATURES.md`, `docs/bugs/`, `docs/waves/`, or `docs/features/` exists, the only skill is `migrate-docs`.

The communication contract uses the names and concepts already in the project. Do not invent a synonym for a term the project already uses. The first sentence to the user states the understood intent, in one sentence. Stop when that sentence is wrong.

One idea per sentence. Be clear and on the point. English follows ASD-STE100. German follows "Deutsch für die Technische Kommunikation" (tekom Deutschland e.V.). Name the standards. Do not copy their text. Keep German and English separate.
