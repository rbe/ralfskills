# Pipeline rules

The shared part is the same in every repository. Change it everywhere or nowhere. This repository's facts go under "This repository" and "Divergences".

## Shared rules

The Makefile is the interface. A laptop and CI run the same targets, and a target does the same thing in both places. The workflow calls `make` and moves artifacts. It holds no other logic. Podman is the only container engine. The toolchain runs in a pinned image, so the host needs make, Podman, git, and gh.

`sdlc.mk` at the repository root is the shared makefile. It is byte-identical to the canonical copy. The project Makefile sets `IMAGE`, `PACKAGE`, and `KEEP_VERSIONS`, includes `sdlc.mk`, and defines the project targets.

There is one workflow, `.github/workflows/ci.yml`. Jobs, in order: `setup`, then `build`, `test`, and `docs` beside each other, then `publish-container` (needs `build` and `test`), then `report`. A repository that ships a release asset adds `publish-github`, which also needs `build` and `test`. Each job runs the make target with its name.

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
