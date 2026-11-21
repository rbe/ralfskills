---
name: onboard
description: Bring a project onto this skill collection in one run. Use when the owner says report and integrate, onboard, adopt, or add the skills to a project, for a new project and for an existing one. Checks the prerequisites, runs migrate-docs when the old board exists, then project-setup in report mode and setup mode, github-pipeline when the project publishes through GitHub, record for the rules the project already follows, and every gate. It stops when a gate fails. It writes no feature.
---

# Onboard

This skill is the order of the other skills. It does no work of its own that a skill below does not own. The skills named here must be installed. Stop and name the missing skill when one is not.

The onboarding of a project is not a slice. It has no history file. Its commits go on the default branch. The owner's request to integrate covers those commits and the push to the remote the project already has. Do not push to another remote.

## Steps

1. Check the prerequisites on this machine. `make --version` runs. `git --version` runs. `podman info` runs. On macOS, a stopped Podman machine fails that command, so start it with `podman machine start`. Stop when one of them fails. Name what is missing and how to install it. Do not install a tool on the host. Once the Makefile has the include, `make doctor` is the same check, and `make setup` runs it first.
2. Read the project before any question. Name the language from the manifest and the file types: `package.json`, `build.gradle`, `go.mod`, `pyproject.toml`, `*.py`, or a shell recipe. Name the old board: the paths in `migrate-docs`, and `AGENTS.md`. Read `Makefile`, `CLAUDE.md`, `README.md`, and `.github/workflows/`. Read the remote with `git remote get-url origin` for the host, the owner, and the name. Read the default branch. Count the tests.
3. Ask the owner only what the files do not tell. Ask one question at a time. The one question that is always open is how the project ships: a binary, a container image, a library package, or with the merge only. A project on `github.com` that ships an image publishes through GitHub.
4. When the old board exists, run `migrate-docs` now. Every other skill stops until it has deleted those paths. Fold `AGENTS.md` into `CLAUDE.md` as that skill says. Commit the board on the default branch and push.
5. Run `project-setup` in report mode. Run `github-pipeline` in report mode when the project publishes through GitHub. Write both reports in the reply, before any change. Name what matches and what is missing.
6. Run `project-setup` in setup mode, in the order that skill gives. The language skill names the tooling target: `make node-tooling`, `make python-tooling`, `make jvm-tooling`, or `make go-tooling`. A language that has no installed skill has no template. Stop and name the language, then ask the owner whether to write the Makefile by hand. Commit the setup, with `.claude/skills/`, `apm.yml`, and `apm.lock.yaml`, on the default branch. Push.
7. When the project publishes through GitHub, run `github-pipeline` in setup mode. Node and Gradle have a template for the whole Makefile and the workflow. For any other language, take the image block of the Makefile from `templates/Makefile.image`, the `Containerfile` template of the language, and `templates/ci.make.yml`. Fill the owner and the name from step 2. Do not leave `OWNER` or `NAME` as a placeholder. Check that `make test` runs the tests after the include switch. Commit and push.
8. Record each rule the project already follows through `record`. An architecture or development rule is an ADR. A small choice is a Decided row. A rule the code already breaks is also a row in `docs/KNOWN_ISSUES.md`. Each existing test gets a Decided row that states the behaviour it proves, and names that row with `id:`. Run `make links`. Commit and push.
9. Run every gate through Make: `make editorconfig`, `make format`, `make lint`, `make test`, `make integration`, `make coverage`, `make ids`, `make toon`, `make links-check`, `make project-report`. A project with a workflow also runs `make ci`. Stop when a gate fails. Fix the cause. Do not loosen a check, and do not skip one.
10. Answer in the reply, in this order: what the project is, what changed in each commit, which gate passed, and which gate did not run and why. Then name what only the owner can do. That list can hold `make auth`, the package permission of the repository on GitHub, the first `vMAJOR.MINOR.PATCH` tag, and the first publish from the Actions tab. When the collection has a tag, say that `ref: <tag>` under the `git:` line of `apm.yml` pins the version, and that `apm update` takes a newer one. The README has the update steps. Then say that the first slice starts with `plan`.

## Do not

- Do not write a feature, a fix, or a refactor in this run.
- Do not pick the language, the shipment, or the owner from a guess. A file or the owner states each one.
- Do not leave a file from the old board beside the new board.
- Do not write a second entry file. `CLAUDE.md` is the only one.
