# Pipeline rules

The shared part is the same in every repository. Change it everywhere or nowhere. This repository's facts go under "This repository" and "Divergences".

## Shared rules

The Make contract is the project-setup skill. Make is the only interface. A person or an agent does the work through Make. `help` is the default goal. A target does the same thing on a laptop and in CI. The required targets are `setup`, `build`, and `test`. Add `docs` only when this repository renders docs, and `login` when it publishes an image. Gradle, npm, Podman, python, and tar run inside those targets.

The GitHub contract is the github-pipeline skill. Podman is the only container engine. The toolchain runs in a pinned image, so the host needs make, Podman, git, and gh. `sdlc.mk` at the repository root implements version, publish tags, cleanup, and report. It is byte-identical to the canonical copy in that skill. The project Makefile sets `IMAGE`, `PACKAGE`, and `KEEP_VERSIONS`, includes `sdlc.mk` before any target, and defines the project targets. That include already provides `help`, so this repository leaves `project.mk` out.

There is one workflow, `.github/workflows/ci.yml`. A step is a checkout, an artifact upload or download, or `run: make <target>`. Jobs, in order: `setup`, then `build`, `test`, and `docs` beside each other, then `publish-container` (needs `build` and `test`), then `report`. A repository that releases a JAR adds `publish-github`, which also needs `build` and `test`. Each job runs the make target with its name.

`publish-*` runs on a push to the default branch and when `workflow_dispatch` selects it. A tag push does not start a run. Any other branch runs through `report` and does not publish. A manual publish runs `build` and `test` first. In-progress runs are cancelled only off the default branch.

The published version is the nearest `vMAJOR.MINOR.PATCH` tag, without the `v`, plus `-` and the GitHub run number. A default-branch publish also tags `latest`, then keeps that run and the next-lower run number on the same `MAJOR.MINOR.PATCH` line. A manual publish from any other ref tags the version only: it does not move `latest` and cleanup deletes nothing. There is no `edge`, `sha-*`, or bare version tag. No such tag, or a nearer pre-release tag, fails the publish. Cleanup does not delete a GHCR version that still carries `latest` or any tag other than `MAJOR.MINOR.PATCH-<run>`. A missing GHCR package (HTTP 404) is an empty list, so the first publish's cleanup does not fail the job. A skipped or failed publish deletes nothing.

Every upload sets `retention-days`: 1 for intermediates, 14 for `report` and rendered docs. `setup` starts with `cleanup-actions-artifacts`, which deletes this repository's other artifacts once they are an hour old. The current run's artifacts stay, and so do `report` and `docs`.

`report` is last. It still runs when an earlier job fails or is skipped. It writes `build/report/index.md`.

Packages and images contain the tested build only. `.containerignore` keeps out `.claude/`, `.cursor/`, `AGENTS.md`, `CLAUDE.md`, and `docs/`.

## This repository

| | |
| --- | --- |
| Image | `ghcr.io/OWNER/NAME` |
| Default branch | `main` |
| Toolchain | Node 24 in the image |

## Divergences

Each entry names the shared rule, what differs, and why.

- Rule: …. Here: …. Why: ….
