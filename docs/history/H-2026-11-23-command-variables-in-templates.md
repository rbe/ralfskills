---
id: H-2026-11-23-command-variables-in-templates
title: The Node and Gradle templates of github-pipeline set command variables
status: closed
adrs: [R-23, R-46, R-71]
skills: [develop, record, review, shell, python]
roadmap: []
proposals: []
---

# The Node and Gradle templates of github-pipeline set command variables

## Plan

The owner approved planned row R-79 and said this project has no users. The two templates set the command variables of the Make contract and define no contract target.

## Develop

`SDLC_OWN_CONTRACT` is removed everywhere. Both templates set the command variables above the include. `container.mk` gained `IMAGE_CONTEXT`, `IMAGE_PREPARE`, and `PUBLISH_PREPARE`. `contract.mk` tests an empty command with `ifeq`. No test was weakened or deleted.

## Review

Gates passed in Podman, including `make test`, `make lint`, and `make ids`. Each template ran in a scratch project with a stub `podman`, under Make 4.3 and Make 3.81, with the same commands. Not run: `make integration` and `make coverage`. Security: no listener and no secret.

## Release

Not invoked: the owner merges this slice.
