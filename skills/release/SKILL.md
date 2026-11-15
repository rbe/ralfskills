---
name: release
description: Ship a binary or a container image. Invoke github-pipeline when the workflow, version, publish, image, cleanup, or retention changes. Invoke project-setup only when that same change adds or overrides a Make target. Do not invoke project-setup on every ship. Invoke record for the Release section.
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
4. A divergence is the rule, what differs, and why. `record` stores it where `github-pipeline` says to write divergences, or as a Decided line when it is not a pipeline divergence.
5. When this task does not ship, the Release section is `Not invoked: this slice does not ship.`
