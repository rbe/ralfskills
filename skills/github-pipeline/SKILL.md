---
name: github-pipeline
description: Apply or check the GitHub delivery contract in setup mode or report mode. One workflow runs setup, then build, test, and docs, then publish, then report. Versions come from a vMAJOR.MINOR.PATCH tag plus the run number. Use setup mode when adding CI, aligning a pipeline, changing publish or versioning, or fixing artifact storage. Setup changes only what is missing or off the contract and leaves a target the project already filled in. Use report mode to fill templates/contract-report.md and name what matches and what is missing, without changing the project. Depends on project-setup because each job name is a Make target. A Make-only repository does not install this skill. The shared makefile is sdlc.mk. No shell scripts.
---

# GitHub pipeline

This skill owns the GitHub contract and the Make that implements it. `sdlc.mk` is that makefile: version, publish tags, cleanup, and report. A project includes the installed file. It does not keep a second copy.

It depends on `project-setup` only because a workflow calls `make`. The job names `setup`, `build`, `test`, and `docs` (when the repository renders docs) are real targets from that contract. `login` is the target the publish job runs, not its own job. A Make-only repository does not install this skill. Podman and XDG paths are `project-setup`. What a shipment may contain is the Report and packaging section of this skill.

## Steps

1. If `docs/BUGS.md`, `docs/WAVES.md`, `docs/FEATURES.md`, `docs/bugs/`, `docs/waves/`, or `docs/features/` exists, stop. Name `migrate-docs`. Do not take a later step.
2. Invoke `record` before creating an id or a document. A write that skips `record` fails this step.
3. Do this skill's work, in the order below. `release` invokes this skill when the change touches the workflow, the version, publish, the image, cleanup, or retention.
4. Ask `record` to add one line under the open history section naming `github-pipeline`. When no history file is open, do not open one.

## Modes

Use one mode. A request that asks for both runs report mode first, then setup mode for the rows that are missing. A row that matches stays as it is.

Report mode is the contract report in `templates/contract-report.md`. The `report` target is a different report: it writes `build/report/index.md` for one pipeline run.

A repository that uses Make and has no GitHub workflow stops here. It installs `project-setup` only. Setup mode adds no workflow there.

| Mode | When | Files |
| --- | --- | --- |
| Setup | Set up a new project that publishes through GitHub, or bring an existing one into line with this contract | Writes only what is missing or off the contract |
| Report | Show the current project against this contract | Reads the project. Writes nothing |

A target is filled in when the project's Makefile gives it a recipe. Setup mode leaves that recipe. On a `project-setup` Makefile the fill-in is also a non-empty `SETUP_CMD`, `BUILD_CMD`, `TEST_CMD`, or `DOCS_CMD`. Those values stay.

### Setup mode

Read:

| File | Where |
| --- | --- |
| `SKILL.md`, `sdlc.mk` | This skill. The project includes `sdlc.mk` from here. Leave this skill's file unchanged |
| `templates/Makefile.node`, `templates/ci.node.yml` | Node toolchain |
| `templates/Makefile.gradle`, `templates/ci.gradle.yml` | Gradle toolchain |
| `templates/pipeline-rules.md` | The source for `docs/pipeline-rules.md` |
| `templates/Containerfile.node`, `templates/Containerfile.gradle`, `templates/Containerfile.python`, `templates/Containerfile.go` | The source for `Containerfile`, by toolchain |
| `templates/ci.make.yml`, `templates/Makefile.image` | The workflow and the image block of a project on the Makefile of its language skill: Python, Go, or another. No Node or Gradle template applies |
| `container.mk` | The image targets of a project with no recipe of its own for them. `sdlc.mk` includes it |
| `templates/containerignore`, `templates/gitignore` | The source for `.containerignore` and `.gitignore` |
| `Makefile` | The project, when present |
| `.github/workflows/` | The project |
| `docs/pipeline-rules.md`, `Containerfile`, `.containerignore`, `.gitignore` | The project, when present |

Write:

| File | Write when |
| --- | --- |
| `Makefile` | `include .claude/skills/github-pipeline/sdlc.mk` is missing or sits after a target, or a required target has no recipe and no command variable. A recipe already in the file stays. Do not write `sdlc.mk` at the repository root |
| `.github/workflows/ci.yml` | No workflow yet: start from the matching template. A `ci.yml` already there: fix a trigger, a permission, a missing `retention-days`, or a `run:` step that is not `make <target>`. A step that is already `make <target>` stays |
| `docs/pipeline-rules.md` | It is missing. Copy the template and fill "This repository". When the file exists, leave "This repository" and "Divergences" as written |
| `Containerfile`, `.containerignore`, `.gitignore` | The file is missing. Copy the template for the toolchain. In `Containerfile`, change the paths and the start command to the ones the project uses. When `.containerignore` or `.gitignore` exists, add only a line of the template that is missing |

The workflow is one file, `.github/workflows/ci.yml`, named `CI`. It calls `make`. `publish-*` runs on a push to the default branch or when `workflow_dispatch` selects that job, and it needs `build` and `test`. The version is the nearest `vMAJOR.MINOR.PATCH` tag, read by `make version`. This mode creates no `v*` tag and adds no tag trigger.

A second workflow file is named in the report. This mode does not delete it and does not add a workflow beside `ci.yml`.

When the Makefile includes `project.mk` or `.claude/skills/project-setup/project.mk`, switch the include to `.claude/skills/github-pipeline/sdlc.mk` and remove the `project.mk` include. `sdlc.mk` already provides `help`, and it includes the contract targets of `project-setup` (`setup`, `build`, `test`, `format`, `lint`, `coverage`, and the others). So the command variables of the language Makefile keep working, and the switch loses no target. A project that has no `project.mk` include and writes its own recipes for those targets sets `SDLC_OWN_CONTRACT = 1` before the include, as the Node and Gradle templates do. Check `make test` after the switch. It must run the tests, not print that there is nothing to do. A root `sdlc.mk` is off the contract. Leave its bytes and name it in the report.

A project on the Makefile of the `python` or `go` skill takes the image block of `templates/Makefile.image`. Fill `OWNER` from `git remote get-url origin`, copy the `Containerfile` template of the language, change `PACKAGE` or `NAME` in it, and use `templates/ci.make.yml` as `.github/workflows/ci.yml`. `make build` then builds the image, runs the smoke check, and saves the image tar. The Node and Gradle templates are for a project that has no language Makefile of its own.

A recipe this mode adds follows Make 3.81. No `.ONESHELL`. No Make 4 function (`$(file ...)`, `$(guile ...)`, `!=`). Each recipe line is one POSIX shell, joined with backslashes. No shell-script wrapper. A shell `$` is `$$`.

### Report mode

Read `templates/contract-report.md` and the Contract test section. Read the project files in the setup table. `make -qp` shows `.DEFAULT_GOAL`. The include path is `.claude/skills/github-pipeline/sdlc.mk`. `git describe --tags --abbrev=0 --match 'v[0-9]*'` shows the tag `version` accepts.

When the repository has no workflow and does not publish through GitHub, fill Applies as yes and leave the checks blank. The verdict is that this skill stays uninstalled.

Fill the skeleton in the reply. `State` is `matches` or `missing`. The verdict lists both. Leave the skill's template blank. Write no project file. Do not copy `sdlc.mk`. Do not run `make publish-container`, `make publish-github`, or a cleanup target.

## Files

This repository is the shared skill collection. Node 24 is the Node template only. A Gradle project uses the JDK in its template. A project diverges only when it has a different output or toolchain, and it writes that down.

| File | Role |
| --- | --- |
| `sdlc.mk` | Version, publish tags, cleanup, and report, and the contract targets of `project-setup` through `contract.mk`. The project includes the installed file |
| `container.mk` | `image`, `image-ci`, and `publish-container` for a project on a language Makefile. `sdlc.mk` includes it unless `SDLC_OWN_CONTRACT = 1` |
| `templates/Makefile.node` | Node app, image only. Node 24 is this template's toolchain. Make contract: `project-setup` |
| `templates/Makefile.gradle` | Gradle app, image plus a JAR release. The JDK image in this file is this template's toolchain. Make contract: `project-setup` |
| `templates/ci.node.yml`, `templates/ci.gradle.yml`, `templates/ci.make.yml` | `.github/workflows/ci.yml` |
| `templates/pipeline-rules.md` | `docs/pipeline-rules.md`. Points at `project-setup` for the Make contract |
| `templates/contract-report.md` | Report mode skeleton. The reply fills it. The file in this skill stays blank |

No shell script is shipped. Version, both cleanups, artifact cleanup, the report, logging, `help`, and `ci` are recipes in `sdlc.mk`. `gh api --jq` does the listing. A short `awk` plan inside the cleanup recipe picks what to keep. That stayed readable, so it did not become a script.

## How a repository uses it

The project Makefile sets variables, includes `sdlc.mk` before any target, then defines project targets. The target names, `help` as the default goal, and the rule that tools run inside targets are the `project-setup` contract.

```make
IMAGE ?= ghcr.io/owner/name
PACKAGE ?= owner/name
KEEP_VERSIONS ?= 2
include .claude/skills/github-pipeline/sdlc.mk

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
| `SDLC_CI` | What `ci` runs, in order. Default `setup build editorconfig format lint test integration coverage docs report`. Drop `docs` when there is no docs target |
| `SDLC_KEEP_ARTIFACTS` | Artifact names the hourly cleanup never deletes. Default `report,docs` |
| `HELP_LEAD` | First line of `make help` |

`$(call SDLC_LOG,job,_job)` tees `_job` to `build/logs/job.log` and writes a failed summary when `_job` fails. The goal has no comma in its name. `_job` is the real recipe.

A recipe that must not run under `make -n` calls `$(THIS_MAKE)`, not `$(MAKE)`. Make executes a recipe that mentions `$(MAKE)` even during a dry run, which would push an image. `ci` uses `$(MAKE)` on purpose, so `make -n ci` walks the child targets and does not publish.

## Targets in sdlc.mk

`help` is the `project-setup` default goal. This file defines it too, so one include is enough. The GitHub recipes are `version`, `publish-tags`, `cleanup-container-versions`, `cleanup-github-releases`, `cleanup-actions-artifacts`, and `report`. `ci` runs `SDLC_CI` and does not publish.

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

`setup`, `build`, and `test` are required names from the `project-setup` contract. `docs` is required only when the repository renders docs, and `login` only when it publishes an image. `help` is the default goal. A target does the same thing locally and in CI. Gradle, npm, Podman, python, and tar run inside those targets. This skill depends on `project-setup` only because the workflow calls `make` and those job names are that contract's targets. `publish-container`, `publish-github`, and `report` are targets this skill adds.

The project also defines `publish-container` and, when it releases a JAR, `publish-github`. `publish-container` pushes every line of `publish-tags` and writes that version to `build/publish-version.txt`. On the default branch those lines are the version and `latest`. A manual publish from any other ref is the version only, and the cleanup targets then exit without deleting. A laptop-only command gets its own name (`dev`, `verify`).

`sdlc.mk` also defines `help`, so a repository that includes it already meets the default goal. That repository does not include `project.mk` as well. The Gradle case is `build`: the job runs `make build`, and that target runs Gradle (`$(GRADLE) assemble` in the template, `./gradlew` when the repo sets `GRADLE=./gradlew`). The publish job runs `make login` before `make publish-container`. `login` reads `REGISTRY_USER` and `REGISTRY_TOKEN` and runs `podman login ghcr.io`.

## Workflow

One file, `.github/workflows/ci.yml`, named `CI`. Job ids are target names from the `project-setup` contract, plus `publish-container`, `publish-github` when the project releases a JAR, and `report`.

```
setup ──┬── build ──┬── publish-container ──┐
        ├── test ───┤                       ├── report
        │           └── publish-github ─────┤
        └── docs ───────────────────────────┘
```

- Trigger: `push` on every branch, and `workflow_dispatch` with a `job` choice. No `pull_request` trigger. No tag trigger. After tagging `vX.Y.Z`, start `publish-container` from the Actions tab.
- `publish-*` runs on a push to the default branch (`github.event.repository.default_branch`) or when that job is selected by hand. A manual publish still runs `build` and `test`. It needs both to have succeeded. A push of a `v*` tag does not publish.
- `report` uses `if: ${{ !cancelled() }}` and is last.
- Cancel in-progress runs only when the push is not the default branch.
- Permissions: `contents: read` at the top, `actions: write` on `setup`, `packages: write` on `publish-container`, `contents: write` on `publish-github`.
- A step is `actions/checkout`, an artifact upload or download, or `run: make <target>`. Nothing else. No `./gradlew`, `npm`, `podman`, `python`, `tar`, `printf`, or `tee` in the YAML. Gradle is `make build`. Registry login is `make login`.
- Workflow `env` holds `IMAGE` and `SDLC_DEFAULT_BRANCH` (`github.event.repository.default_branch`). The Makefile sets `IMAGE` to that same image name. The Node template's `env` also holds `NODE_VERSION` at 24. That line is the Node template only. A Gradle project uses the JDK in its template. A project diverges by toolchain and writes that down.
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

Each job uploads `report-<job>` with `build/logs` and `build/summaries`, and `test` also uploads results and `build/coverage`. That coverage file is the diff-cover report of the lines this change touched, not a repository-wide percentage. The test job runs `make editorconfig`, `make format`, `make lint`, `make test`, `make integration`, and `make coverage`. `report` downloads `report-*` into `build/inputs` and runs `make report`. `build/report/index.md` is the entry point.

A shipment is a binary or a container image. The image copies named files, not the work tree. `.containerignore` keeps out `.git`, `.github`, `.claude/`, `apm_modules/`, `CLAUDE.md`, `docs/`, `build/`, `node_modules`, `data/`, `.env`, `.env.*`, and `*.tar`. `templates/containerignore` is that list. Example data ships only from `examples/` when the path and the name say it is an example. `.claude/skills/` is committed so Make can include it, and the image still excludes `.claude/`. `.gitignore` keeps build output, image tars, `data/`, and `.env` out of git.

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
- the Makefile does not include `.claude/skills/github-pipeline/sdlc.mk` before any target, or a root `sdlc.mk` is the include
- `make test`, `make build`, or `make setup` runs no recipe, that is, the include switch lost a contract target

Do not weaken the test to make a run pass. Fix the pipeline, or record a real divergence.

Report mode records each of these in `templates/contract-report.md`. Setup mode repairs a missing workflow rule. It leaves a target the project already filled in. A Make-only repository is not a failed test: that repository does not install this skill.
