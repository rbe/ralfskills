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
| R-53 | In a product repository, when the owner answers a choice that is expensive to reverse, `plan` asks `record` for an ADR id. `record` writes `docs/adr/<id>.md` with the status `Accepted`. The Plan section cites that id. A choice that is cheap to reverse stays a Decided entry. |
| R-54 | `develop` runs `make toon` and reads `docs/adr/index.toon` before it edits. It opens each ADR whose status is `Accepted` and whose `skills` names a skill this slice uses. `review` opens the same ADRs. A change that breaks an accepted ADR is a finding. |
| R-55 | An accepted ADR replaces a skill rule only when the ADR is a divergence. A divergence names the rule, what differs, and why. An ADR that differs from a skill rule and does not name these three is a finding in `review`. What `github-pipeline` says is not a divergence stays not allowed. |
| R-56 | `record` owns the ADR status. The values are `Accepted` and `Superseded`. A new ADR names the ADR it replaces in `supersedes`. `record` then sets the status of the replaced ADR to `Superseded`. `plan`, `develop`, and `review` follow only an accepted ADR. The project report does not list a superseded ADR as an id with no test. |
