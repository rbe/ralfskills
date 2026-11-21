# ralfskills

Skills for [Microsoft APM](https://github.com/microsoft/apm). This repository is a [skill collection](https://microsoft.github.io/apm/reference/package-types/#skill-collection-skillsnameskillmd): each skill is `skills/<name>/SKILL.md`. There is no `SKILL.md` at the repository root, so APM does not treat the repository as one skill.

Install so the files land in `.claude/skills/`. That is the APM target `claude`. Make includes `project.mk` from that path, or `sdlc.mk` when `github-pipeline` is installed. `CLAUDE.md` is the only entry file in a project that uses these skills.

## Skills

| Skill | What it covers |
| --- | --- |
| [plan](skills/plan/SKILL.md) | Grill. Ask one question at a time. Write a history file to start now, or a proposal to implement later |
| [develop](skills/develop/SKILL.md) | Implement the slice with the installed language skill |
| [review](skills/review/SKILL.md) | Gates and the installed subskills, after the change |
| [release](skills/release/SKILL.md) | Commit, push, merge when CI passed, and close the task. Invokes `github-pipeline` when delivery changes |
| [record](skills/record/SKILL.md) | Ids, the board, the history file, the ADRs and their status, the ADR index, the decision log, and this collection's requirements index |
| [onboard](skills/onboard/SKILL.md) | The order of the other skills for a project that adopts this collection. Say `report and integrate` |
| [project-report](skills/project-report/SKILL.md) | Generated requirements map, architecture review, and development review |
| [migrate-docs](skills/migrate-docs/SKILL.md) | The only skill that reads an old board. Other skills stop until it has deleted those files |
| [project-setup](skills/project-setup/SKILL.md) | Writes `CLAUDE.md` from its template when the file is missing. Make is the only interface. `help` is the default goal. EditorConfig, one formatter, one linter, unit tests, one integration entry, and a diff-cover report are targets |
| [github-pipeline](skills/github-pipeline/SKILL.md) | One GitHub workflow. Versions from a `vMAJOR.MINOR.PATCH` tag plus the run number |
| [security](skills/security/SKILL.md) | Questions before a slice, checks after |
| [privacy](skills/privacy/SKILL.md) | Personal data, before and after |
| [ux-ui-design](skills/ux-ui-design/SKILL.md) | Interaction. Product tokens stay in a project skill |
| [api-design](skills/api-design/SKILL.md) | HTTP, and the public API of a module or a library. The route list stays in a project skill |
| [node](skills/node/SKILL.md) | JavaScript and TypeScript |
| [python](skills/python/SKILL.md) | Python |
| [shell](skills/shell/SKILL.md) | POSIX shell inside a recipe |
| [jvm](skills/jvm/SKILL.md) | Java, Groovy, Grails, and Gradle |
| [go](skills/go/SKILL.md) | Go |

The `name` in each skill's frontmatter matches its directory. A project installs the stages, `record`, `project-setup`, `project-report`, the language skills it uses, and the subskills it wants. It installs `github-pipeline` when it publishes through GitHub. It installs `migrate-docs` when the old board is still present, and it runs that skill before the others.

`project-setup` and `github-pipeline` each have setup mode and report mode, written in the skill. Setup mode changes only what is missing or off the contract. Report mode names what matches and what is missing, and it changes nothing.

`make toon` writes the ADR index and the skill index for a product repository. In this collection it writes `docs/requirements-index.toon` and the skill index, and it does not create `docs/adr/`. `make decision-log` writes `build/decision-log.md` from the ADRs and the decisions. `project.mk` and `sdlc.mk` include these targets from `record` when the skill is installed, and `make setup` runs `make toon` first. Every Python command, including a one-off `make py ARGS='...'`, runs in Podman on the machine where Make runs. Set `PYTHON_IMAGE` before the include to pick the version. The host does not need Python.

## The cycle

A request goes through `plan`, `develop`, `review`, and `release`. A new or vague request starts at `plan`. A fix that names a source file, a failing test, or a known issue starts at `develop`. `release` commits the slice on one branch, pushes it, merges it into the default branch when CI passed, and asks `record` to close the task. With `github-pipeline` installed, that merge publishes.

`record` keeps the decisions. A choice that is expensive to reverse becomes an ADR in `docs/adr/`. A small choice is an entry in `docs/DECISIONS.md`. `develop` and `review` open each accepted ADR that names a skill the slice uses, so an agent follows the rules of this one project. `make decision-log` writes `build/decision-log.md`, the same decisions as one document for a person. Each id in a document is a link to its item, written by `make links`.

## Start

1. Add the `apm.yml` below and run `apm install`. APM must run first, because the skills are not on the machine before it.
2. Tell the agent: `report and integrate`. The [onboard](skills/onboard/SKILL.md) skill carries the order, for a new project and for an existing one.

`onboard` does these steps, and each one is a skill that you can also start alone:

1. It checks that Make, Git, and Podman run on the machine.
2. It reads the project: the language, the old board, the remote, and the tests. It asks you only what the files do not tell, such as how the project ships.
3. It runs `migrate-docs` when `docs/BUGS.md`, `docs/WAVES.md`, `docs/FEATURES.md`, or their directories, or `AGENTS.md` exist, and commits the new board.
4. It runs `project-setup` in report mode, then in setup mode. Setup mode asks how the project ships, copies the Makefile template of the language, and runs the tooling target of that language: `make node-tooling`, `make python-tooling`, `make jvm-tooling`, or `make go-tooling`. It writes `CLAUDE.md`, `.editorconfig`, and `.gitignore`, and commits with `.claude/skills/`, `apm.yml`, and `apm.lock.yaml`.
5. When the project publishes through GitHub, it runs `github-pipeline`: one workflow, a `Containerfile`, and the targets of the pipeline.
6. It records each rule the project already follows as an ADR or a Decided row, and gives each existing test the `id:` of the row it proves.
7. It runs every gate. It stops when one fails.

Then the first slice starts with `plan`.

## Update

This collection has tags named `vMAJOR.MINOR.PATCH`. A project that wants a fixed version sets `ref: v0.1.0` under the `git:` line of `apm.yml`. Without `ref`, APM follows the default branch and prints a warning.

To take a newer version:

1. Change `ref` to the new tag. Skip this step when the project has no `ref`.
2. Run `apm update`. `apm update --dry-run` shows the plan and changes nothing. `apm update --yes` skips the question, for CI. `apm install --update` is deprecated in APM 0.36.1.
3. Run `make toon` and `make links`, because a new skill can add rows to the indexes and the links.
4. Run the gates: `make editorconfig`, `make format`, `make lint`, `make test`, and `make ci` when the project has a workflow.
5. Commit `.claude/skills/`, `apm.yml`, and `apm.lock.yaml` together, on the default branch.

`apm update` overwrites a skill file that a person changed in `.claude/skills/`. Keep project rules in a project skill or in `CLAUDE.md`, not in an installed file. A new Makefile template does not change the `Makefile` of the project. Run `project-setup` in report mode to see what a new version adds.

## How APM loads them

The `apm.yml` of a project needs `name` and `version`. APM refuses the file without them. `apm install` reads every `skills/<name>/` directory and copies it to `.claude/skills/<name>/`, including makefiles, `references/`, `scripts/`, and `templates/` inside the skills. That was tested with APM 0.36.1: nine skills installed into a sample project, and `make toon`, `make ids`, `make project-report`, and `make decision-log` ran there. This collection itself has no root `apm.yml`. APM does not need one in a skill collection.

```yaml
name: my-project
version: 0.1.0
targets:
  - claude
dependencies:
  apm:
    - git: rbe/ralfskills
      # ref: <tag or commit>   pins the version
      skills:
        - plan
        - develop
        - review
        - release
        - record
        - project-report
        - project-setup
        - onboard
        - github-pipeline   # when the project publishes through GitHub
        - migrate-docs      # when the old board is still present
        - node              # or python, jvm, go: the language skills the project uses
        - shell
        - security
```

A Make-only repository leaves `github-pipeline` out. A repository that still has `docs/BUGS.md`, `docs/WAVES.md`, `docs/FEATURES.md`, `docs/bugs/`, `docs/waves/`, or `docs/features/` adds `migrate-docs` and runs it first.

`apm install` does not write `CLAUDE.md`. `apm compile` for the target `claude` keeps a `CLAUDE.md` that a person wrote and prints a warning. That was tested with APM 0.36.1. `project-setup` owns the entry file. APM adds `apm_modules/` to `.gitignore`. It also creates `.apm-local/`, which has its own `.gitignore`.

Install one skill with `--skill`. Repeat the flag to add another. `apm install rbe/ralfskills --skill '*'` installs every skill again.
