---
id: H-2026-11-21-onboard-and-shared-contract
title: One onboard skill, one shared contract, and a delivery that fits every language
status: closed
adrs: []
skills: [plan, develop, review, record, project-setup, github-pipeline, onboard, shell]
decisions: [D-13]
proposals: []
issues: []
---

# One onboard skill, one shared contract, and a delivery that fits every language

## Plan

The owner asked for a trial review: can a project start with the skills from APM and the words `report and integrate`? The review found three blockers. The owner then asked for items 1 to 3 as one slice.

Boundary: `project-setup` owns the contract targets. `github-pipeline` owns the delivery targets. `onboard` owns only the order of the other skills.

Pattern: one shared file for the contract targets, which both entry makefiles include. One image block for every language. One entry skill.

## Develop

`contract.mk` in `project-setup` holds the contract targets that were in `project.mk`. `project.mk` keeps the help target and includes `contract.mk`. [R-71](../REQUIREMENTS.md#r-71) states it.

`sdlc.mk` includes `contract.mk` and `container.mk` unless the project sets `SDLC_OWN_CONTRACT = 1`. The Node and Gradle templates set it, because they write their own recipes. D-13 records the choice.

`container.mk` has `image`, `image-ci`, and `publish-container`, and does not depend on the language. `image-ci` deletes the old tar before `podman save`, so a second run does not fail. The Node template has the same line.

New templates: `Containerfile.python`, `Containerfile.go`, `Makefile.image`, and `ci.make.yml`. `contract-report.md` has a row that checks the recipes of `setup`, `build`, and `test` after the include.

`onboard` is the new skill. It has ten steps and a `Do not` list. [R-70](../REQUIREMENTS.md#r-70) states it. The README has a `Start` section, and `CLAUDE.md` names the skill.

One unit test read `project.mk` for the `project-report:` target. It now reads `contract.mk`.

## Review

Every gate passed through Make in Podman: `make links`, `make format`, `make lint`, `make test`, `make integration`, `make editorconfig`, `make coverage`, `make test-changed`, `make ids`, `make toon`, `make links-check`, `make project-report`, and `make decision-log`.

Trial runs earlier in this slice: a Python project and a Go project on the GitHub path ran `make ci` with the new templates. The Node and Gradle templates print no override warning.

security: the workflow takes the same permissions as before. No new secret, no listener. The image runs with the smoke check only.

privacy: no personal data.

ux-ui-design: no screen.

api-design: not HTTP. `OWNER`, `NAME`, `IMAGE`, `CONTAINERFILE`, `SMOKE_ARGS`, and `SDLC_OWN_CONTRACT` are the interface of the includes.

No finding. Left alone: no fresh agent ran `report and integrate` with `onboard` yet. The JVM language did not run on the language-neutral path. No run on macOS or Windows with a Podman machine.

## Release

Committed on the working branch. This slice does not merge it.
