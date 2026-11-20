# ralfskills

Skills for [Microsoft APM](https://github.com/microsoft/apm). This repository is a [skill collection](https://microsoft.github.io/apm/reference/package-types/#skill-collection-skillsnameskillmd): each skill is `skills/<name>/SKILL.md`. There is no `SKILL.md` at the repository root, so APM does not treat the repository as one skill.

Install so the files land in `.claude/skills/`. That is the APM target `claude`. Make includes `project.mk` and `sdlc.mk` from that path. `CLAUDE.md` is the only entry file in a project that uses these skills.

## Skills

| Skill | What it covers |
| --- | --- |
| [plan](skills/plan/SKILL.md) | Grill. Ask one question at a time. Write a history file to start now, or a proposal to implement later |
| [develop](skills/develop/SKILL.md) | Implement the slice with the installed language skill |
| [review](skills/review/SKILL.md) | Gates and the installed subskills, after the change |
| [release](skills/release/SKILL.md) | Commit, push, merge when CI passed, and close the task. Invokes `github-pipeline` when delivery changes |
| [record](skills/record/SKILL.md) | Ids, the board, the history file, the ADRs and their status, the ADR index, the decision log, and this collection's requirements index |
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

The `name` in each skill's frontmatter matches its directory. A project installs the stages, `record`, `project-setup`, `project-report`, the language skills it uses, and the subskills it wants. It installs `github-pipeline` when it publishes through GitHub. It installs `migrate-docs` when the old board is still present, and it runs that skill before the others.

`project-setup` and `github-pipeline` each have setup mode and report mode, written in the skill. Setup mode changes only what is missing or off the contract. Report mode names what matches and what is missing, and it changes nothing.

`make toon` writes the ADR index and the skill index for a product repository. In this collection it writes `docs/requirements-index.toon` and the skill index, and it does not create `docs/adr/`. `make decision-log` writes `build/decision-log.md` from the ADRs and the decisions. `project.mk` and `sdlc.mk` include that target from `record` when the skill is installed, and `make setup` runs it first. Every Python command, including a one-off `make py ARGS='...'`, runs in Podman on the machine where Make runs. Set `PYTHON_IMAGE` before the include to pick the version. The host does not need Python.

## The cycle

A request goes through `plan`, `develop`, `review`, and `release`. A new or vague request starts at `plan`. A fix that names a file or a failing test starts at `develop`. `release` commits the slice on one branch, pushes it, merges it into the default branch when CI passed, and asks `record` to close the task. With `github-pipeline` installed, that merge publishes.

`record` keeps the decisions. A choice that is expensive to reverse becomes an ADR in `docs/adr/`. A small choice is an entry in `docs/DECISIONS.md`. `develop` and `review` open each accepted ADR that names a skill the slice uses, so an agent follows the rules of this one project. `make decision-log` writes `build/decision-log.md`, the same decisions as one document for a person.

## A new project

1. Add the `apm.yml` below and run `apm install`.
2. Ask the agent to run `project-setup` in setup mode. It writes `CLAUDE.md` from the template, the `Makefile`, and `.editorconfig`.
3. When the project publishes through GitHub, ask for `github-pipeline` in setup mode.
4. Start the first slice with `plan`.

## An existing project

1. Add the `apm.yml` below and run `apm install`.
2. When `docs/BUGS.md`, `docs/WAVES.md`, `docs/FEATURES.md`, `docs/bugs/`, `docs/waves/`, or `docs/features/` exists, run `migrate-docs` first.
3. Ask for `project-setup` in report mode, then in setup mode. Setup mode writes only what is missing. It keeps a `CLAUDE.md` and a target the project already has.
4. Record each rule the project already follows as an ADR through `record`. Name the skills it governs in `skills`.

## How APM loads them

`apm install` reads every `skills/<name>/` directory and copies it to `.claude/skills/<name>/`, including makefiles, `references/`, `scripts/`, and `templates/` inside the skills. A root `apm.yml` is optional. APM fills in metadata when the file is absent.

```yaml
targets:
  - claude
dependencies:
  apm:
    - git: rbe/ralfskills
      skills:
        - plan
        - develop
        - review
        - release
        - record
        - project-report
        - project-setup
        - github-pipeline
        - node
```

A Make-only repository leaves `github-pipeline` out. A repository that still has `docs/BUGS.md`, `docs/WAVES.md`, `docs/FEATURES.md`, `docs/bugs/`, `docs/waves/`, or `docs/features/` adds `migrate-docs` and runs it first.

The APM documentation says that `apm compile` writes a `CLAUDE.md` at the project root for the target `claude`. This collection ships no APM instructions, and `project-setup` owns the entry file. Check the diff of `CLAUDE.md` after a compile.

Install one skill with `--skill`. Repeat the flag to add another. `apm install rbe/ralfskills --skill '*'` installs every skill again.
