---
name: project-setup
description: Apply or check the Make contract in setup mode or report mode. Make is the only interface, help is the default goal, and a target does the same thing locally and in CI. Use setup mode when adding a Makefile, naming setup, build, test, docs, or login, moving Gradle, npm, Podman, python, or tar into a target, or installing Homebrew tools such as jq. Setup changes only what is missing or off the contract and leaves a target the project already filled in. Use report mode to fill templates/contract-report.md and name what matches and what is missing, without changing the project. Stands alone. The shared makefile is project.mk. A repository that does not publish through GitHub installs only this skill.
---

# Project setup

Make is the only interface. A person or an agent does the work through Make.

`help` is the default goal. `make` with no target prints the targets.

A target does the same thing locally and in CI. A command that only makes sense on a laptop gets its own name (`dev`, `verify`).

This skill stands alone. Version tags, GHCR, and cleanup are the `github-pipeline` skill. A repository that uses Make and has no GitHub workflow installs this skill only.

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
| `SKILL.md`, `project.mk` | This skill. `project.mk` is the copy source |
| `Makefile`, `project.mk` | The project, when present |
| `sdlc.mk` | The project, only to see whether that include already provides `help` |

Write:

| File | Write when |
| --- | --- |
| `project.mk` | It is missing, or it is not byte-identical to this skill's copy. The sha256 is in Check |
| `Makefile` | It is missing, the include is missing or sits after a target, or a required variable is unset |

`project.mk` provides `help`, `setup`, `build`, `test`, and, when the variables say so, `docs` and `login`. The Makefile sets variables and includes `project.mk` before any target. Setup mode does not define `setup`, `build`, or `test` again. A second definition replaces the recipe from `project.mk`.

The project fills a target in with `SETUP_CMD`, `BUILD_CMD`, or `TEST_CMD`, and with `DOCS_CMD` when it renders docs. Set a variable only when it is empty and the toolchain is already in the project (`package.json`, Gradle, python, or tar). A value already set stays. When the Makefile already has a recipe for that target, leave the recipe and leave the command variable empty. The report names that empty variable as missing.

When the project's `project.mk` differs from this skill and holds a recipe the Makefile does not, copy that command into the matching variable first. An existing Makefile value wins. Then replace `project.mk` with this skill's file.

`setup` installs `jq` through Homebrew when `brew` is on `PATH`, then any names in `BREW_TOOLS`. A tool already on `PATH` stays. Leave `BREW_TOOLS` when the project set it. The system `make` stays GNU Make 3.81.

Set `RENDER_DOCS` and `DOCS_CMD` when the repository renders docs and those variables are empty. Set `PUBLISH_IMAGE` when an image is published and that variable is empty. A value the project set stays. Command variables stay above the include. A shell `$` in a command is `$$`.

A line this mode adds follows Make 3.81. No `.ONESHELL`. No Make 4 function (`$(file ...)`, `$(guile ...)`, `!=`). Each recipe line is one POSIX shell, joined with backslashes. No shell-script wrapper.

When the include is `sdlc.mk`, leave `project.mk` out. That file already provides `help`, and the project targets belong to `github-pipeline`.

This mode does not add `sdlc.mk`, a workflow, or a `v*` tag.

When the required command variables are set, or the Makefile already defines those targets, run `make setup`. That target installs `jq`. When a required variable is still empty, leave the run for later. The stub names the variable. Do not run `brew install` outside `make setup`.

### Report mode

Read `templates/contract-report.md` in this skill, this skill's `project.mk`, and the Check section. Read the project's `Makefile` and `project.mk`. `make -qp` shows `.DEFAULT_GOAL`. Compare the project's `project.mk` to the sha256 in Check.

Fill the skeleton in the reply. `State` is `matches` or `missing`. The verdict lists both. Leave the skill's template blank. Write no project file, do not copy `project.mk`, and do not run `make setup`, `make build`, `make test`, `make docs`, `make login`, or `brew install`.

## Target names

A project that uses this standard uses these names.

| Target | When |
| --- | --- |
| `setup` | Always. Install the standard tools, then resolve dependencies |
| `build` | Always. Produce the artifact |
| `test` | Always. Run the tests |
| `docs` | Only when the repository renders docs |
| `login` | Only when an image is published. Reads `REGISTRY_USER` and `REGISTRY_TOKEN` and logs in to `REGISTRY` |

Gradle, npm, Podman, python, and tar run inside those targets. The step that runs them is `make setup`, `make build`, `make test`, `make docs`, or `make login`. The Gradle case is `build`: that target runs Gradle. `setup` installs the standard tools and resolves dependencies, `test` runs the tests, `docs` runs the renderer, and `login` logs in to the registry.

## Standard implementation

`project.mk` is what is the same in every repository: `help`, the tool install in `setup`, the `build`, `test`, and `docs` stubs, and `login` when an image is published. Copy it to the repository root unchanged.

The project Makefile sets the variables, then includes `project.mk` before any target. A `##` comment on the target line is the text `help` prints. `help` lists `setup`, `build`, and `test`. It lists `docs` and `login` only when those targets exist.

```make
SETUP_CMD = npm ci
BUILD_CMD = npm run build
TEST_CMD = npm test
RENDER_DOCS = 1
DOCS_CMD = node scripts/render-docs.mjs docs build/docs
PUBLISH_IMAGE = 1
include project.mk
```

Set these before the include. `RENDER_DOCS` and `PUBLISH_IMAGE` are read while `project.mk` is parsed.

| Variable | Meaning |
| --- | --- |
| `HELP_LEAD` | First line of `make help`. `project.mk` has a default |
| `BREW_TOOLS` | Extra tools `setup` installs. `jq` is always on the list |
| `SETUP_CMD` | How this project resolves dependencies. Empty fails `setup` |
| `BUILD_CMD` | How this project produces the artifact. Empty fails `build` |
| `TEST_CMD` | How this project runs the tests. Empty fails `test` |
| `RENDER_DOCS` | `1` when this repository renders docs. Otherwise there is no `docs` target |
| `DOCS_CMD` | The renderer. Empty fails `docs` |
| `PUBLISH_IMAGE` | `1` when an image is published. Otherwise there is no `login` target |
| `REGISTRY` | Registry host for `login`. Default `ghcr.io` |

A shell `$` in a command is `$$`.

`setup` installs tools through Homebrew when `brew` is on `PATH`. The list is `jq`, then `BREW_TOOLS`. A tool already on `PATH` stays as it is. When `brew` is missing, `setup` prints `brew install` and the tool names, then continues when those tools are already on `PATH`. A missing tool and no Homebrew fails `setup` before `SETUP_CMD`.

`build`, `test`, and `docs` are stubs. `login` reads `REGISTRY_USER` and `REGISTRY_TOKEN` and runs `podman login`.

Defining `setup`, `build`, or `test` again replaces the recipe from `project.mk`.

`project.mk` marks `help`, `setup`, `build`, and `test` `.PHONY`, and `docs` and `login` when they exist. A `build/` directory would otherwise satisfy `build`. `project.mk` sets `.DEFAULT_GOAL` to `help`.

A repository that includes `sdlc.mk` from `github-pipeline` already has `help` and does not also include `project.mk`. That repository defines its own project targets.

## Make 3.81

GNU Make 3.81, including the macOS system make.

- No `.ONESHELL`. Each recipe line is one POSIX shell. Join a recipe with backslashes.
- No Make 4 functions (`$(file ...)`, `$(guile ...)`, `!=`).
- No shell-script wrapper. The recipe in the Makefile is the command.

## Check

The repository fails this contract when:

- `make` with no goal runs anything other than `help`
- `setup`, `build`, or `test` is missing, `docs` is missing while the repository renders docs, `login` is missing while an image is published, or one of those targets is not `.PHONY`
- `SETUP_CMD`, `BUILD_CMD`, or `TEST_CMD` is empty, or `DOCS_CMD` is empty while the repository renders docs
- a person, an agent, or a workflow step runs Gradle, npm, Podman, python, or tar directly instead of `make setup`, `make build`, `make test`, `make docs`, or `make login`
- `project.mk` is not byte-identical to this skill's copy (sha256 `7314d971bbf2e0068a65c52363b62a70a201d1d8dacecedb67aa6f72a2419aa8`), or the project Makefile includes it after the first target
- the Makefile uses `.ONESHELL` or a Make 4 function, or the standard targets call out to a shell script
- `setup` does not install `jq` through Homebrew when `brew` is on `PATH`. A tool already on `PATH` stays. A missing tool and no Homebrew fails `setup`

Report mode records each of these in `templates/contract-report.md`. Setup mode repairs a missing file, a missing include, or an empty command variable. It leaves a target the project already filled in.
