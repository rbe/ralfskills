# The Makefile of a project that includes sdlc.mk

The project Makefile sets variables, includes `sdlc.mk` before any target, and then defines the project targets.

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

## Variables to set before the include

| Variable | Meaning |
| --- | --- |
| `IMAGE` | `ghcr.io/owner/name`, no tag |
| `PACKAGE` | GitHub `owner/name`. The default is `GITHUB_REPOSITORY` |
| `KEEP_VERSIONS` | The number of versions to keep, including the version just published. The default is 2 |
| `SDLC_JOBS` | The jobs that the pipeline report lists. Add `publish-github` when that job exists |
| `SDLC_CI` | The targets that `ci` runs, in order. The default is `setup build editorconfig format lint test integration coverage docs report`. Remove `docs` when there is no docs target |
| `SDLC_KEEP_ARTIFACTS` | The artifact names that the hourly cleanup does not delete. The default is `report,docs` |
| `HELP_LEAD` | The first line of `make help` |
| `SDLC_OWN_CONTRACT` | Set to 1 when the project writes its own recipes for the contract targets and the image targets. `sdlc.mk` then includes neither `contract.mk` of `project-setup` nor `container.mk` |
| `GH_BASE_IMAGE`, `GH_VERSION` | The base image and the release of the GitHub CLI image |
| `OWNER`, `NAME` | The GitHub owner and the repository name. `ci-status` passes them as `-R owner/name`, and `pull-request` and `pull-request-merge` put them in the REST route, because the image has no Git |

## Recipe helpers

- `$(call SDLC_LOG,job,_job)` writes the output of `_job` to `build/logs/job.log`. If `_job` fails, it writes a failed summary. `_job` is the real recipe. The goal name contains no comma.
- If a recipe must not run under `make -n`, it calls `$(THIS_MAKE)`, not `$(MAKE)`. Make executes a recipe line that contains `$(MAKE)` during a dry run, and that line could push an image.
- `ci` calls `$(MAKE)`, so that `make -n ci` goes through the child targets. `ci` does not publish.
- `$(GH)` runs the GitHub CLI in the image that `make gh-image` builds. The token is `GH_TOKEN` or `GITHUB_TOKEN` of the environment, on a laptop and in CI.
- The cleanup recipes list with `gh api --jq`. An `awk` plan inside the cleanup recipe selects the versions to keep.

## Targets of sdlc.mk

| Target | Contract |
| --- | --- |
| `help` | The default goal. It lists every target that has a `##` comment. One include is sufficient, because `sdlc.mk` defines `help` |
| `version` | Prints `MAJOR.MINOR.PATCH-run` from `git describe`. `PRINT=tag` prints the `vX.Y.Z` tag. Fails when there is no strict tag, when a pre-release tag is nearer, or when `GITHUB_RUN_NUMBER` is not set |
| `ci` | Runs `SDLC_CI` in order. Does not publish |
| `report` | Writes `build/report/index.md` from logs, summaries, and `JOB_RESULT_*` |
| `publish-tags` | Prints the version. Prints `latest` only when the ref is the default branch or `GITHUB_REF` is not set |
| `gh-image` | Builds the image of the GitHub CLI, one time |
| `ci-status` | Prints the result of the CI run for `HEAD`, or for `SHA=<sha>`. Fails when the run failed, did not finish, or does not exist. `WAIT=1` waits for the end |
| `pull-request` | Opens a pull request from the current branch to `DEFAULT_BRANCH`. `TITLE` and `BODY` are optional. Prints the open one when it exists. Uses `gh api` REST routes only |
| `pull-request-merge` | Merges the pull request of the current branch when all check runs of its head commit passed. No check run, or one that did not pass, stops the merge. `WAIT=1` waits for the checks. Uses `gh api` REST routes only |
| `cleanup-container-versions` | On the default branch, keeps this run and the next-lower run on the same `MAJOR.MINOR.PATCH` line. A missing package is an empty list. Does not delete `latest` or a tag that is not `MAJOR.MINOR.PATCH-<run>`. Off the default branch, deletes nothing |
| `cleanup-github-releases` | On the default branch, keeps this release and the next-lower run. Does not delete a name that is not `MAJOR.MINOR.PATCH-<run>`. Off the default branch, deletes nothing |
| `cleanup-actions-artifacts` | Deletes the artifacts of this repository that are older than one hour, except `report`, `docs`, and the artifacts of this run |

`DRY_RUN=1` makes each cleanup print what it would delete. The cleanup then only reads, so it is safe against the real API.

## Targets of container.mk

`container.mk` provides `image`, `image-ci`, and `publish-container` for a project on a language Makefile.

## Targets that the project defines

- `setup`, `build`, and `test` are required names of the `project-setup` contract. `docs` is required only when the repository renders docs. `login` is required only when the repository publishes an image.
- `login` reads `REGISTRY_USER` and `REGISTRY_TOKEN` and runs `podman login ghcr.io`. The publish job runs `make login` before `make publish-container`.
- `publish-container` pushes every line of `make publish-tags` and writes the version to `build/publish-version.txt`. On the default branch the lines are the version and `latest`. From any other ref the only line is the version, and the cleanup targets exit and delete nothing.
- `publish-github` exists when the project releases a JAR or a binary.
- In a Gradle project, `make build` runs Gradle: `$(GRADLE) assemble` in the template.
- A command for the laptop only gets its own name, for example `dev` or `verify`.
