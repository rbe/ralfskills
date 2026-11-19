# Requirements

Each requirement is one statement this skill set must fulfill.

| Id | Statement |
| --- | --- |
| R-1 | A test names the requirement it proves with `id:` in its header or metadata. |
| R-2 | `make test` is the full suite. `make test-changed` runs the tests that cover the files in the diff. |
| R-3 | The file has the requirements-to-tests map, the architecture review, and the development review. |
| R-4 | The `name` in a skill's frontmatter matches its directory. |
| R-5 | This is the only skill that reads the old board. |
| R-6 | `make toon` writes the ADR index and the skill index through `$(PYTHON)`. |
| R-7 | Name the boundary and the pattern for this slice: who owns state, and what may call what. |
| R-8 | Do not report done until make lint and make test have passed. |
| R-9 | The formatter and the linter are existing tools the language skill names. |
| R-10 | `api-design` asks what is exported, what stays internal, and what the resource, the verb, and the status on success are. |
| R-11 | `help` is the default goal. `make` with no target prints the targets. |
| R-12 | `coverage` writes `build/coverage/diff.md` through diff-cover, for the lines this change touched. |
| R-13 | A retired id is never issued again. |
| R-14 | Evaluate architecture, scalability, and code quality against the constraints of this system. Prefer the smallest design that stays operable and maintainable. When a choice is expensive to reverse, name the options, recommend one, and wait. Otherwise implement it in small modules. |
| R-15 | A product repository keeps in-progress work in `docs/ROADMAP.md` and a rule in `docs/adr/`. |
