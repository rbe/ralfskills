---
name: project-setup
description: Apply or check the Make contract in setup mode or report mode. Make is the only interface, help is the default goal, and a target does the same thing locally and in CI. Use setup mode when adding a Makefile, naming setup, build, test, docs, or login, moving Gradle, npm, Podman, python, or tar into a target, or installing Homebrew tools such as jq. Setup also writes CLAUDE.md from the template when it is missing, EditorConfig, and the targets format, lint, integration, coverage, and test-changed. The formatter and the linter are existing tools the language skill names. Setup changes only what is missing or off the contract and leaves a target the project already filled in. Use report mode to fill templates/contract-report.md and name what matches and what is missing, without changing the project. Stands alone. The shared makefile is project.mk. A repository that does not publish through GitHub installs only this skill.
---

# Project setup

Make is the only interface. A person or an agent does the work through Make.

`help` is the default goal. `make` with no target prints the targets.

A target does the same thing locally and in CI. A command that only makes sense on a laptop gets its own name (`dev`, `verify`).

This skill stands alone. Version tags, GHCR, and cleanup are the `github-pipeline` skill. A repository that uses Make and has no GitHub workflow installs this skill only.

## Steps

1. If `docs/BUGS.md`, `docs/WAVES.md`, `docs/FEATURES.md`, `docs/bugs/`, `docs/waves/`, or `docs/features/` exists, stop. Name `migrate-docs`. Do not take a later step.
2. Invoke `record` before creating an id or a document. A write that skips `record` fails this step.
3. Do this skill's work, in the order below. `plan` invokes this skill once, when the Makefile is missing, and again only when a slice adds or overrides a target.
4. Ask `record` to add one line under the open history section naming `project-setup`. When no history file is open, do not open one.

## Modes

Use one mode. A request that asks for both runs report mode first, then setup mode for the rows that are missing. A row that matches stays as it is.

| Mode | When | Files |
| --- | --- | --- |
| Setup | Set up a new project, or bring an existing one into line with this contract | Writes only what is missing or off the contract |
| Report | Show the current project against this contract | Reads the project. Writes nothing |

A repository that uses Make and has no GitHub workflow uses this skill only.

A target is filled in when its command variable has a non-empty value, or the project's Makefile gives that target a recipe. Setup mode leaves that value and that recipe.

### Setup mode

Read:

| File | Where |
| --- | --- |
| `SKILL.md`, `project.mk` | This skill. The project includes `project.mk` from here |
| `templates/CLAUDE.md` | The source for the project's entry file |
| `CLAUDE.md` | The project, when present |
| `Makefile` | The project, when present |
| `.claude/skills/github-pipeline/sdlc.mk` | Present when that skill is installed. That include already provides `help` |

Write:

| File | Write when |
| --- | --- |
| `Makefile` | It is missing, the include is missing or sits after a target, or a required variable is unset |
| `CLAUDE.md` | It is missing. Copy `templates/CLAUDE.md` and fill each bracket from the project and from `docs/skill-index.toon`. When the file exists, leave its text and add only a paragraph of the template that is missing |

`CLAUDE.md` is the only entry file. It names the stages, the installed language skills and subskills, each project skill, where each record is kept, and the communication contract. The template is the one source of that text for a project. An existing project keeps what its `CLAUDE.md` already says.

A new project has no toolchain yet. Ask which installed language skill the project uses. Copy the Makefile template of that skill: `templates/Makefile.python` in `python`, or `templates/Makefile.node` in `node`. The template names each command variable. Create the manifest of the project through a Make target, not on the host. An existing project gets only the lines of the template it lacks.

Run `make toon` before the entry file is written. The brackets of the template are filled from `docs/skill-index.toon`.

A recipe the project already has stays, unless it runs a toolchain on the host. A recipe that runs Gradle, npm, node, or python on the host is off the contract. Rewrite it to the command variable, and keep what it does.

A project with no dependency to resolve, no artifact to build, or no integration entry sets that command to `true`. `true` is a filled-in value.

`.gitignore` has the lines `build/`, `apm_modules/`, `docs/adr/index.toon`, and `docs/skill-index.toon`. Add a line that is missing. Commit `.claude/skills/`, `apm.yml`, and `apm.lock.yaml`. The Makefile includes files from `.claude/skills/`, so a clone needs them.

Do not write `project.mk` at the repository root. A root `project.mk` is off the contract. Leave its bytes and name it in the report.

`project.mk` provides `help`, `setup`, `build`, `test`, and, when the variables say so, `docs` and `login`. The Makefile sets variables and includes `.claude/skills/project-setup/project.mk` before any target. Setup mode does not define `setup`, `build`, or `test` again. A target repeated after the include, with a recipe, replaces the recipe from `project.mk`.

The project fills a target in with `SETUP_CMD`, `BUILD_CMD`, or `TEST_CMD`, and with `DOCS_CMD` when it renders docs. Set a variable only when it is empty and the toolchain is already in the project (`package.json`, Gradle, python, or tar). A value already set stays. When the Makefile already has a recipe for that target, leave the recipe and leave the command variable empty. The report names that empty variable as missing.

`setup` installs `jq` through Homebrew when `brew` is on `PATH`, then any names in `BREW_TOOLS`. A tool already on `PATH` stays. Leave `BREW_TOOLS` when the project set it. The system `make` stays GNU Make 3.81.

Set `RENDER_DOCS` and `DOCS_CMD` when the repository renders docs and those variables are empty. Set `PUBLISH_IMAGE` when an image is published and that variable is empty. A value the project set stays. Command variables stay above the include. A shell `$` in a command is `$$`.

A line this mode adds follows Make 3.81. No `.ONESHELL`. No Make 4 function (`$(file ...)`, `$(guile ...)`, `!=`). Each recipe line is one POSIX shell, joined with backslashes. No shell-script wrapper.

When the Makefile includes `.claude/skills/github-pipeline/sdlc.mk`, leave this skill's include out. That file already provides `help`, and the project targets belong to `github-pipeline`.

This mode does not add `sdlc.mk`, a workflow, or a `v*` tag.

When the required command variables are set, or the Makefile already defines those targets, run `make setup`. That target installs `jq`. When a required variable is still empty, leave the run for later. The stub names the variable. Do not run `brew install` outside `make setup`.

### Report mode

Read `templates/contract-report.md` in this skill, this skill's `project.mk`, and the Check section. Read the project's `Makefile` and `CLAUDE.md`. `make -qp` shows `.DEFAULT_GOAL`. The include path is `.claude/skills/project-setup/project.mk`, or `.claude/skills/github-pipeline/sdlc.mk` when that file provides `help`.

Fill the skeleton in the reply. `State` is `matches` or `missing`. The verdict lists both. Leave the skill's template blank. Write no project file, do not copy `project.mk`, and do not run `make setup`, `make build`, `make test`, `make docs`, `make login`, or `brew install`.

## Target names

A project that uses this standard uses these names.

| Target | When |
| --- | --- |
| `setup` | Always. Install the standard tools, then resolve dependencies |
| `build` | Always. Produce the artifact |
| `test` | Always. Run the unit tests |
| `editorconfig` | Always. Check the tree with editorconfig-checker |
| `format` | Always. Check the files with the one formatter |
| `format-fix` | Always. Rewrite the files with that formatter |
| `lint` | Always. Run the one linter |
| `integration` | Always. The one integration entry |
| `coverage` | Always. diff-cover report of the lines this change touched |
| `test-changed` | Always. The tests that cover the files in the diff. CI still runs `test` |
| `project-report` | When that skill is installed. Writes `build/project-report.md` |
| `docs` | Only when the repository renders docs |
| `login` | Only when an image is published. Reads `REGISTRY_USER` and `REGISTRY_TOKEN` and logs in to `REGISTRY` |

Gradle, npm, Podman, python, and tar run inside those targets. The step that runs them is `make setup`, `make build`, `make test`, `make docs`, or `make login`. The Gradle case is `build`: that target runs Gradle. `setup` installs the standard tools and resolves dependencies, `test` runs the tests, `docs` runs the renderer, and `login` logs in to the registry.

## Standard implementation

`project.mk` is what is the same in every repository: `help`, the tool install in `setup`, the `build`, `test`, and `docs` stubs, and `login` when an image is published. The project includes the installed file. It does not keep a second copy.

The project Makefile sets the variables, then includes `.claude/skills/project-setup/project.mk` before any target. A `##` comment on the target line is the text `help` prints. `help` lists `setup`, `build`, `test`, `test-changed`, and `project-report`. It lists `docs` and `login` only when those targets exist. A target added after the include is the project's. A target repeated there, with a recipe, overrides the included recipe.

```make
SETUP_CMD = npm ci
BUILD_CMD = npm run build
TEST_CMD = npm test
FORMAT_CMD = npm exec -- prettier --check .
LINT_CMD = npm exec -- eslint .
INTEGRATION_CMD = npm run integration
RENDER_DOCS = 1
DOCS_CMD = node scripts/render-docs.mjs docs build/docs
PUBLISH_IMAGE = 1
include .claude/skills/project-setup/project.mk

# Project targets and overrides.
```

Set these before the include. `RENDER_DOCS` and `PUBLISH_IMAGE` are read while `project.mk` is parsed.

| Variable | Meaning |
| --- | --- |
| `HELP_LEAD` | First line of `make help`. `project.mk` has a default |
| `BREW_TOOLS` | Extra tools `setup` installs. `jq` is always on the list |
| `SETUP_CMD` | How this project resolves dependencies. Empty fails `setup` |
| `BUILD_CMD` | How this project produces the artifact. Empty fails `build` |
| `TEST_CMD` | How this project runs the unit tests. Empty fails `test` |
| `FORMAT_CMD` | The one formatter, in check mode. It changes no file. Empty fails `format`. The language skill names the tool |
| `FORMAT_FIX_CMD` | The same formatter in write mode. `make format-fix` rewrites the files. Empty fails `format-fix` |
| `LINT_CMD` | The one linter. Empty fails `lint`. The language skill names the tool |
| `INTEGRATION_CMD` | The one integration entry. Empty fails `integration` |
| `COVERAGE_CMD` | Writes `build/coverage/diff.md` and the coverage map `test-changed` reads. Empty fails `coverage` |
| `DIFF_COVER_IMAGE` | The image that runs diff-cover. It has git and Python. Default `docker.io/library/python:3.13` |
| `TEST_CHANGED_CMD` | Runs the tests that cover the diff. Empty fails `test-changed`. The selection is coverage, not a hand-kept list |
| `PROJECT_REPORT_CMD` | Writes `build/project-report.md`. `report.mk` in `project-report` sets it when that skill is installed and the project did not set it. Empty fails `project-report` |
| `RENDER_DOCS` | `1` when this repository renders docs. Otherwise there is no `docs` target |
| `DOCS_CMD` | The renderer. Empty fails `docs` |
| `PUBLISH_IMAGE` | `1` when an image is published. Otherwise there is no `login` target |
| `REGISTRY` | Registry host for `login`. Default `ghcr.io` |

A shell `$` in a command is `$$`.

`setup` installs tools through Homebrew when `brew` is on `PATH`. The list is `jq`, then `BREW_TOOLS`. A tool already on `PATH` stays as it is. When `brew` is missing, `setup` prints `brew install` and the tool names, then continues when those tools are already on `PATH`. A missing tool and no Homebrew fails `setup` before `SETUP_CMD`.

`build`, `test`, and `docs` are stubs. `login` reads `REGISTRY_USER` and `REGISTRY_TOKEN` and runs `podman login`.

Defining `setup`, `build`, or `test` again replaces the recipe from `project.mk`.

`project.mk` marks `help`, `setup`, `build`, `test`, `test-changed`, `project-report`, `editorconfig`, `format`, `lint`, `integration`, and `coverage` `.PHONY`, and `docs` and `login` when they exist. A `build/` directory would otherwise satisfy `build`. `project.mk` sets `.DEFAULT_GOAL` to `help` after the fragments it includes. `podman-python.mk`, `tools.mk`, `test-changed.mk`, `record`'s `index.mk`, and `project-report`'s `report.mk` set the same goal and do not set another. A project Makefile does not set `.DEFAULT_GOAL` to another target.

A repository that includes `.claude/skills/github-pipeline/sdlc.mk` already has `help` and does not also include `project.mk`. That repository defines its own project targets. `test-changed.mk` beside `project.mk` holds the `test-changed` target. Both includes read it, so that repository has `test-changed` too. `project-report` ships the selection for Python, Node, and the JVM. The language skill names the command. Empty, the target fails and names the variable.

## Podman and local paths

`make build`, `make test`, and `make run` call Podman, on a laptop and in CI. Docker is not a second engine. A command that still runs on the host is a divergence: the rule, what differs, and why.

Python is the same rule. `podman-python.mk` defines `$(PYTHON)`. An agent does not run `python3` on the host. A one-off command on this machine is `make py ARGS='...'`. A command variable uses `=` and `$(PYTHON)`. Set `PYTHON_IMAGE` before the include to pick the version.

Config, data, state, and cache use the XDG directories on macOS and Linux. The variables are `XDG_CONFIG_HOME`, `XDG_DATA_HOME`, `XDG_STATE_HOME`, and `XDG_CACHE_HOME`. Unset, those are `~/.config`, `~/.local/share`, `~/.local/state`, and `~/.cache`.

What a shipment may contain is `github-pipeline`. A Make-only repository that ships a binary follows the same limit: the binary, and example data only from `examples/` when the path and the name say it is an example.

## Make 3.81

GNU Make 3.81, including the macOS system make.

- No `.ONESHELL`. Each recipe line is one POSIX shell. Join a recipe with backslashes.
- No Make 4 functions (`$(file ...)`, `$(guile ...)`, `!=`).
- No shell-script wrapper. The recipe in the Makefile is the command.

## Quality targets

Setup mode adds these when they are missing. Stop at the first step that cannot be finished.

1. Write `.editorconfig` from `templates/editorconfig` when the file is missing. `editorconfig` runs editorconfig-checker. Stop when the file cannot be written. Do not take a later step.
2. `format` is one formatter for each language, the tool the language skill names. The formatter does not format `.claude/`, `apm_modules/`, `build/`, or `docs/`. The scripts of `record` read the board line by line. `format` checks, and `format-fix` rewrites. Set `FORMAT_CMD` when it is empty and that tool is already the project's. Stop when a second formatter is present, or when this step cannot name the tool. Do not write a formatter. Do not take a later step.
3. `lint` is one linter for each language, the tool the language skill names. Set `LINT_CMD` the same way. Stop when a second linter is present, or when this step cannot name the tool. Do not write a linter. Do not take a later step.
4. `test` runs the unit tests. Leave an integration test out of `TEST_CMD`. Stop when the unit tests have no command and no recipe. Do not take a later step.
5. `integration` is the one integration entry. Set `INTEGRATION_CMD` when it is empty. Stop when a second integration target exists. Do not take a later step.
6. `coverage` writes `build/coverage/diff.md` through diff-cover, for the lines this change touched. It does not apply a repository-wide percentage. `COVERAGE_CMD` produces that report and the coverage map. The language skill names the coverage tool that feeds diff-cover.
7. `test-changed` runs the tests that cover the files in the diff. The selection is the coverage of those files. Stop when the selection is a hand-kept list. Do not take a later step. `make test` stays the full suite. A green `test-changed` does not replace `make test`. CI runs `make test`.
8. A test names the requirement it proves with `id:` in its header or metadata. The id is an ADR id or a decision id. When an existing test has no id, ask `record` for a Decided row that states the behaviour the test proves, and name that row in the test. One row can serve several tests. Stop when a test has no id. Do not take a later step. The id is not a path.
9. When `project-report` is installed, `make project-report` writes `build/project-report.md`. Stop when that file is missing or hand-edited. Do not take a later step. Hand-editing it is a defect. The file holds the requirements-to-tests map, the architecture review, and the development review.

## Check

The repository fails this contract when:

- `make` with no goal runs anything other than `help`
- `CLAUDE.md` is missing, or it does not name the stages, the installed language skills and subskills, and the communication contract
- `setup`, `build`, or `test` is missing, `docs` is missing while the repository renders docs, `login` is missing while an image is published, or one of those targets is not `.PHONY`
- `SETUP_CMD`, `BUILD_CMD`, or `TEST_CMD` is empty, or `DOCS_CMD` is empty while the repository renders docs
- a person, an agent, or a workflow step runs Gradle, npm, Podman, python, or tar directly instead of `make setup`, `make build`, `make test`, `make docs`, or `make login`
- the Makefile does not include `.claude/skills/project-setup/project.mk` before any target, unless it includes `.claude/skills/github-pipeline/sdlc.mk` instead, or a root `project.mk` is still the include
- the Makefile uses `.ONESHELL` or a Make 4 function, or the standard targets call out to a shell script
- `setup` does not install `jq` through Homebrew when `brew` is on `PATH`. A tool already on `PATH` stays. A missing tool and no Homebrew fails `setup`
- `.editorconfig` is missing, or `editorconfig` does not run editorconfig-checker
- `format` or `lint` is missing, a second formatter or a second linter is a target, or either target runs a linter or formatter written for this project
- `integration` is missing or is not the only integration entry
- `coverage` does not write `build/coverage/diff.md` for the lines this change touched, or the result is a repository-wide percentage
- `test-changed` is missing, it selects tests from a hand-kept list, or CI runs `test-changed` in place of `test`
- a test has no `id:` in its header or metadata
- `project-report` is installed and `make project-report` does not write `build/project-report.md`, or that file is hand-edited
- CI runs a formatter, a linter, a test, or coverage by any command other than `make <target>`

Report mode records each of these in `templates/contract-report.md`. Setup mode repairs a missing file, a missing include, or an empty command variable. It leaves a target the project already filled in.
