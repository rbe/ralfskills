---
name: project-setup
description: Apply or check the Make contract. Make is the only interface, help is the default goal, and a target does the same thing locally and in CI. Use when adding a Makefile, naming setup, build, test, docs, or login, or moving Gradle, npm, Podman, python, or tar into a target. Stands alone. The shared makefile is project.mk (help and the standard targets). A repository that does not publish through GitHub installs only this skill.
---

# Project setup

Make is the only interface. A person or an agent does the work through Make.

`help` is the default goal. `make` with no target prints the targets.

A target does the same thing locally and in CI. A command that only makes sense on a laptop gets its own name (`dev`, `verify`).

This skill stands alone. Version tags, GHCR, and cleanup are the `github-pipeline` skill. A repository that uses Make and has no GitHub workflow installs this skill only.

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
