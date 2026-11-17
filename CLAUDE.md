# ralfskills

This repository is the skill collection. `CLAUDE.md` is the only entry file.

Stages, in order: `plan`, `develop`, `review`, `release`. `record` writes every id and every board document. `project-setup` is the Make contract. `github-pipeline` is the delivery contract, and `release` invokes it when delivery changes.

Language skills: `node`, `python`, `shell`, `jvm`. Subskills `plan` asks and `review` checks: `security`, `privacy`, `ux-ui-design`, `api-design`. A project skill is an extra name listed here.

`plan` names who owns state and what may call what. `develop` is not done until `make lint` and `make test` pass. The linter is the one the language skill names. `make coverage` lists the lines the change touched.

The board is `docs/ROADMAP.md`, `docs/KNOWN_ISSUES.md`, `docs/DECISIONS.md`, `docs/adr/`, `docs/proposals/`, and `docs/history/`. `make toon` writes `docs/adr/index.toon` and `docs/skill-index.toon`. Run it before reading either index.

If `docs/BUGS.md`, `docs/WAVES.md`, `docs/FEATURES.md`, `docs/bugs/`, `docs/waves/`, or `docs/features/` exists, the only skill is `migrate-docs`.

The communication contract uses the names and concepts already in the project. Do not invent a synonym for a term the project already uses. The first sentence to the user states the understood intent, in one sentence. Stop when that sentence is wrong.

One idea per sentence. Be clear and on the point. English follows ASD-STE100. German follows "Deutsch für die Technische Kommunikation" (tekom Deutschland e.V.). Name the standards. Do not copy their text. Keep German and English separate.
