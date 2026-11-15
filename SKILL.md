---
name: common-sdlc
description: Apply or check the common SDLC setup. Make is the interface, one GitHub workflow runs setup then build, test, and docs, then publish, then report, and versions come from vMAJOR.MINOR.PATCH git tags plus the run number. Use when adding CI or a Makefile, aligning a pipeline, renaming targets, changing publish or versioning, or fixing artifact storage. The shared logic is one makefile, sdlc.mk, plus Node and Gradle templates. No shell scripts.
---

# Common SDLC

Developers and agents use Make. Pipelines follow one blueprint. A project diverges only when it has a different output or toolchain, and it writes that down.

| File | Role |
| --- | --- |
| `sdlc.mk` | Shared makefile. Copy it to the repo root unchanged |
| `templates/Makefile.node` | Node app, image only |
| `templates/Makefile.gradle` | Gradle app, image plus a JAR release |
| `templates/ci.node.yml`, `templates/ci.gradle.yml` | `.github/workflows/ci.yml` |
| `templates/pipeline-rules.md` | `docs/pipeline-rules.md` |

No shell script is shipped. Version, both cleanups, artifact cleanup, the report, logging, `help`, and `ci` are recipes in `sdlc.mk`. `gh api --jq` does the listing. A short `awk` plan inside the cleanup recipe picks what to keep. That stayed readable, so it did not become a script.

## How a repository uses it

The project Makefile sets variables, includes `sdlc.mk` before any target, then defines project targets.

```make
IMAGE ?= ghcr.io/owner/name
PACKAGE ?= owner/name
KEEP_VERSIONS ?= 2
include sdlc.mk

setup: ## Match CI: install
	@$(call SDLC_LOG,setup,_setup)
_setup:
	@set -eu; ... ; printf '# setup\n\n...\n' > build/summaries/setup.md
```

Set these before the include:

| Variable | Meaning |
| --- | --- |
| `IMAGE` | `ghcr.io/owner/name`, no tag |
| `PACKAGE` | GitHub `owner/name`. Defaults to `GITHUB_REPOSITORY` |
| `KEEP_VERSIONS` | How many versions to keep, including the one just published. Default 2 |
| `SDLC_JOBS` | Jobs the report lists. Add `publish-github` here when that job exists |
| `SDLC_CI` | What `ci` runs, in order. Default `setup build test docs report`. Drop `docs` when there is no docs target |
| `SDLC_KEEP_ARTIFACTS` | Artifact names the hourly cleanup never deletes. Default `report,docs` |
| `HELP_LEAD` | First line of `make help` |

`$(call SDLC_LOG,job,_job)` tees `_job` to `build/logs/job.log` and writes a failed summary when `_job` fails. The goal has no comma in its name. `_job` is the real recipe.

A recipe that must not run under `make -n` calls `$(THIS_MAKE)`, not `$(MAKE)`. Make executes a recipe that mentions `$(MAKE)` even during a dry run, which would push an image. `ci` uses `$(MAKE)` on purpose, so `make -n ci` walks the child targets and does not publish.

## Targets in sdlc.mk

| Target | Contract |
| --- | --- |
| `help` | Default goal. Lists every target that has a `##` comment |
| `version` | Prints `MAJOR.MINOR.PATCH-run` from `git describe`. `PRINT=tag` prints the `vX.Y.Z` tag. Fails with no strict tag, a nearer pre-release tag, or no `GITHUB_RUN_NUMBER` |
| `ci` | Runs `SDLC_CI` in order. Does not publish |
| `report` | Writes `build/report/index.md` from logs, summaries, and `JOB_RESULT_*` |
| `publish-tags` | Prints the version, and `latest` only when the ref is the default branch or `GITHUB_REF` is unset |
| `cleanup-container-versions` | On the default branch, keeps this run and the next-lower run on that line. A missing package is an empty list. Does not delete `latest` or any non-rolling tag. Off the default branch, deletes nothing |
| `cleanup-github-releases` | On the default branch, keeps this release and the next-lower run. Never deletes a name that is not `MAJOR.MINOR.PATCH-<run>`. Off the default branch, deletes nothing |
| `cleanup-actions-artifacts` | Deletes this repo's artifacts older than one hour, except `report`, `docs`, and this run |

`DRY_RUN=1` prints what a cleanup would delete and deletes nothing.

The project defines `setup`, `build`, `test`, `docs`, `publish-container`, and, when it ships a release, `publish-github`. `publish-container` pushes every line of `publish-tags` and writes that version to `build/publish-version.txt`. On the default branch those lines are the version and `latest`. A manual publish from any other ref is the version only, and the cleanup targets then exit without deleting. `build` and `test` do the same work on a laptop and in CI. A laptop-only command gets its own name (`dev`, `verify`).

A developer or an agent can do everything the pipeline does through Make alone. Every workflow step that runs a tool (`gradle` or `./gradlew`, `npm`, `podman`, `python`, `tar`) is a Make target in the repository Makefile, not a shared target in `sdlc.mk`. The Gradle case is `build`: the job runs `make build`, and that target runs Gradle (`$(GRADLE) assemble` in the template, `./gradlew` when the repo sets `GRADLE=./gradlew`). The job does not call Gradle itself. `setup` resolves dependencies, `test` runs the test task, `docs` runs the renderer, and `publish-container` builds and pushes the image. Registry login is `login`: it reads `REGISTRY_USER` and `REGISTRY_TOKEN` and runs `podman login ghcr.io`. The publish job calls `make login` before `make publish-container`.

## Workflow

One file, `.github/workflows/ci.yml`, named `CI`. Job ids are the target names.

```
setup ──┬── build ──┬── publish-container ──┐
        ├── test ───┤                       ├── report
        │           └── publish-github ─────┤
        └── docs ───────────────────────────┘
```

- Trigger: `push` on every branch, and `workflow_dispatch` with a `job` choice. No `pull_request` trigger. No tag trigger. After tagging `vX.Y.Z`, start `publish-container` from the Actions tab.
- `publish-*` runs on a push to the default branch (`github.event.repository.default_branch`) or when that job is selected. It needs `build` and `test` to have succeeded.
- `report` uses `if: ${{ !cancelled() }}` and is last.
- Cancel in-progress runs only when the push is not the default branch.
- Permissions: `contents: read` at the top, `actions: write` on `setup`, `packages: write` on `publish-container`, `contents: write` on `publish-github`.
- A step is `actions/checkout`, an artifact upload or download, or `run: make <target>`. Nothing else. No `./gradlew`, `npm`, `podman`, `python`, `tar`, `printf`, or `tee` in the YAML. Gradle is `make build`. Registry login is `make login`.
- Workflow `env` holds `IMAGE`, `SDLC_DEFAULT_BRANCH` (`github.event.repository.default_branch`), and the toolchain version. The Makefile sets `IMAGE` to that same image name.
- Pin one runner label, `ubuntu-26.04`.

`setup` runs `make cleanup-actions-artifacts` before it uploads. Do not upload a Gradle home or a whole `build/` directory. `test` runs beside `build`. Between jobs, pass the tested JAR or the image tar, not the workspace. Gradle, npm, and tar run inside the matching Make target, so a laptop runs the same command the job runs.

## Versioning

`version` runs `git describe --tags --abbrev=0 --match 'v[0-9]*'` and accepts only `vMAJOR.MINOR.PATCH`. A nearer `v1.2.0-rc.1` fails the publish even if an older release tag exists. A shallow clone fetches tags once. A default-branch publish also tags `latest`. A manual publish from any other ref does not. There is no `edge`, `sha-*`, or bare `1.2.0` tag. After a default-branch push, cleanup keeps that run and the next-lower run number on the same `MAJOR.MINOR.PATCH` line, not the next older upload time. It does not delete a GHCR version that still carries `latest` or any tag other than `MAJOR.MINOR.PATCH-<run>`. HTTP 404 for a missing package is an empty list, so the first cleanup does not fail the job.

Tag the default branch, push the tag, then run the publish job by hand. A tag push does not publish, because that would publish the same commit twice and the cleanup would then drop the real former version.

## Retention

The artifact quota is shared by every repository on the account. One repo that keeps large artifacts for 90 days blocks the others.

- Every upload sets `retention-days`. Intermediates: 1. `report` and rendered docs: 14.
- `cleanup-actions-artifacts` deletes everything else from this repo once it is an hour old. `report` and `docs` stay until retention. The current run stays.
- `DRY_RUN=1` is safe to run against the real API. It only reads.

## Report and packaging

Each job uploads `report-<job>` with `build/logs` and `build/summaries`, and `test` also uploads results and coverage. `report` downloads `report-*` into `build/inputs` and runs `make report`. `build/report/index.md` is the entry point.

`.containerignore` lists `.git`, `.github`, `.claude/`, `.cursor/`, `AGENTS.md`, `CLAUDE.md`, `docs/`, `build/`, `node_modules`, `data/`, `.env`, `.env.*`, and `*.tar`. The runtime image copies named files, not `COPY . .`. `.gitignore` keeps build output, image tars, `data/`, and `.env` out of git. Whether `.claude/` is tracked is the repo's choice. The image exclusion comes from `.containerignore`.

## Required files

`AGENTS.md` states the product, that the Makefile is the interface, that Podman is the only engine, the publish rule, and the packaging exclusion. `docs/pipeline-rules.md` comes from the template. `docs/BUGS.md`, `docs/WAVES.md`, and `docs/FEATURES.md` are the backlog. They live in `docs/`, not at the root. Also `Containerfile`, `.containerignore`, `Makefile`, `sdlc.mk`, and `.github/workflows/ci.yml`.

## Divergence

Allowed when the project really differs, and written under "Divergences" as the rule, what differs, and why:

- `publish-github` for a JAR or binary release. No `docs` job when there is nothing to render. No `publish-container` for a library.
- A host JDK or host Python, set with one variable such as `GRADLE=./gradlew`, when containerising the tool costs more than it gains.
- Gradle may build the image in `publish-container` from the tested JAR instead of passing an image tar.
- Extra laptop targets (`dev`, `verify`) that no job calls.

Not allowed: a second name for the same target, logic in the YAML, Docker instead of Podman, an upload without `retention-days`, publishing on a tag push or from a branch, a publish that skips `test`, or a version that does not come from `version`.

## Contract test

The repo's own test reads the workflow, the Makefile, and `sdlc.mk`. It fails when:

- there is not exactly one workflow, or the job ids and `needs` differ from the graph
- a `run:` step is not `make <target>`, including a step that runs `./gradlew`, `npm`, `podman login`, `python`, or `tar` instead of `make build`, `make login`, `make setup`, `make test`, `make docs`, or `make publish-container`
- an upload omits `retention-days`, or an intermediate is kept more than 1 day, or `report` is kept more than 14
- `publish-*` is not limited to the default branch or the dispatch input, or it does not need `build` and `test`
- `report` is not last or lacks `!cancelled()`
- `sdlc.mk` is not byte-identical to this skill's copy. Its sha256 is `45c6cf23664d030c61f0fedd2d0639cd9dc2dc7bb03c14167dce61fed9d495d6`

Do not weaken the test to make a run pass. Fix the pipeline, or record a real divergence.
