---
name: project-setup
description: Apply or check the Make contract. Make is the only interface, help is the default goal, and a target does the same thing locally and in CI. Use when adding a Makefile, naming setup, build, test, docs, or login, or moving Gradle, npm, Podman, python, or tar into a target. Stands alone. The shared makefile is project.mk (help, and the include point). A repository that does not publish through GitHub installs only this skill.
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
| `setup` | Always. Resolve dependencies |
| `build` | Always. Produce the artifact |
| `test` | Always. Run the tests |
| `docs` | Only when the repository renders docs |
| `login` | Only when an image is published. Reads `REGISTRY_USER` and `REGISTRY_TOKEN` and logs in to that registry |

Gradle, npm, Podman, python, and tar run inside those targets. The step that runs them is `make setup`, `make build`, `make test`, `make docs`, or `make login`. The Gradle case is `build`: that target runs Gradle. `setup` resolves dependencies, `test` runs the tests, `docs` runs the renderer, and `login` logs in to the registry.

## Standard implementation

What is the same in every repository is `help`, and the include point for a shared makefile. This skill ships `project.mk`. Copy it to the repository root unchanged.

The project Makefile is the include point. It includes `project.mk` before any target, then defines the project targets. A `##` comment on the target line is the text `help` prints.

```make
include project.mk

.PHONY: setup build test

setup: ## Resolve dependencies
	@set -eu; ...

build: ## Produce the artifact
	@set -eu; ...

test: ## Run the tests
	@set -eu; ...
```

The `.PHONY` line is part of that include point. A `build/` directory would otherwise satisfy `build`. When the repository renders docs or publishes an image, add `docs` or `login` to that line and define the target.

Set `HELP_LEAD` before the include when the first line of `help` should differ. `project.mk` sets `.DEFAULT_GOAL` to `help`.

`project.mk` stops there. A repository that includes `sdlc.mk` from `github-pipeline` already has `help` and does not also include `project.mk`.

## Make 3.81

GNU Make 3.81, including the macOS system make.

- No `.ONESHELL`. Each recipe line is one POSIX shell. Join a recipe with backslashes.
- No Make 4 functions (`$(file ...)`, `$(guile ...)`, `!=`).
- No shell-script wrapper. The recipe in the Makefile is the command.

## Check

The repository fails this contract when:

- `make` with no goal runs anything other than `help`
- `setup`, `build`, or `test` is missing, `docs` is missing while the repository renders docs, `login` is missing while an image is published, or one of those targets is not `.PHONY`
- a person, an agent, or a workflow step runs Gradle, npm, Podman, python, or tar directly instead of `make setup`, `make build`, `make test`, `make docs`, or `make login`
- `project.mk` is not byte-identical to this skill's copy (sha256 `11f27507cf4faf2be1e3bbd8be78e4048fc139b0eb192a3f1e6aeb26d4eff746`), or the project Makefile includes it after the first target
- the Makefile uses `.ONESHELL` or a Make 4 function, or the standard targets call out to a shell script
