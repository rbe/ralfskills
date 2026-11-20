---
name: release
description: Ship a reviewed slice and close the task. Use after review, for a fix or a feature. Commit on one branch, push, merge into the default branch when CI passed, then ask record to close the task. A shipment is a binary or a container image. Invoke github-pipeline when the workflow, version, publish, image, cleanup, or retention changes. Invoke project-setup only when that same change adds or overrides a Make target. Do not invoke project-setup on every ship. Invoke record for the Release section.
---

# Release

## Steps

1. If `docs/BUGS.md`, `docs/WAVES.md`, `docs/FEATURES.md`, `docs/bugs/`, `docs/waves/`, or `docs/features/` exists, stop. Name `migrate-docs`. Do not take a later step.
2. Invoke `record` before creating an id or a document. A write that skips `record` fails this step.
3. Do the work below, in order.
4. Ask `record` to write the Release section, or one sentence that says why `release` was not invoked. `record` rejects a history file missing Plan, Develop, Review, or Release.

## Work

1. Read `project-setup` for Podman, XDG paths, and what a shipment may contain. Do not restate those rules.
2. When the change touches the workflow, the version, publish, the image, cleanup, or retention, invoke `github-pipeline`.
3. When that same change adds or overrides a Make target, invoke `project-setup`. Otherwise do not invoke `project-setup`.
4. A divergence is the rule, what differs, and why. `record` stores it where `github-pipeline` says to write divergences, or as an ADR with the section `## Divergence` when it is not a pipeline divergence.
5. When this task does not ship, the Release section is `Not invoked: this slice does not ship.` Ask `record` to close the task. Do not take a later step.
6. Read the Review section. Stop when `make lint` or `make test` failed or did not run, or when a finding is neither fixed nor a known-issue id. Do not take a later step.
7. The slice is one branch. Commit the change and the board documents together. The first line of the commit message is one sentence that says what the system now does. Push the branch.
8. CI runs the same Make targets on that push. Stop when CI fails. Do not take a later step. A repository with no workflow runs `make lint`, `make test`, and `make integration` on this machine instead.
9. Ask the owner before the merge when the request did not ask for a ship. Then merge the branch into the default branch. Do not create a `v*` tag. The owner tags a version.
10. A push to the default branch publishes when `github-pipeline` is installed. Write the published version in the Release section. A Make-only repository ships with the target its `CLAUDE.md` names.
11. Ask `record` to close the task.
