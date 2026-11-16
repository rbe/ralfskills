# ralfskills

This repository is the skill collection. `CLAUDE.md` is the only entry file.

Stages, in order: `plan`, `develop`, `review`, `release`. `record` writes every id and every board document. `project-report` generates the requirements-to-tests map and the architecture and development reviews. `project-setup` is the Make contract. `github-pipeline` is the delivery contract, and `release` invokes it when delivery changes.

Language skills: `node`, `python`, `shell`, `jvm`. Subskills `plan` asks and `review` checks: `security`, `privacy`, `ux-ui-design`, `api-design`. A project skill is an extra name listed here.

`plan` names who owns state and what may call what. `develop` is not done until `make lint` and `make test` pass. The linter is the one the language skill names. `make test` is the full suite. `make test-changed` runs the tests that cover the diff. `make coverage` lists the lines the change touched. `make project-report` writes the generated report.

The board is `docs/ROADMAP.md`, `docs/KNOWN_ISSUES.md`, `docs/DECISIONS.md`, `docs/adr/`, `docs/proposals/`, and `docs/history/`. `make toon` writes `docs/adr/index.toon` and `docs/skill-index.toon`. Run it before reading either index.

If `docs/BUGS.md`, `docs/WAVES.md`, `docs/FEATURES.md`, `docs/bugs/`, `docs/waves/`, or `docs/features/` exists, the only skill is `migrate-docs`.
