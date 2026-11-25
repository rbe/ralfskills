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

The owner approved the planned row R-79 and said that this project is not in use, so the change keeps no backward compatibility. The owner asked that the two templates set the command variables of the Make contract, define no contract target again, and keep every toolchain in Podman.

The templates `Makefile.node` and `Makefile.gradle` of `skills/github-pipeline/templates` are not a copy of the language templates `skills/node/templates/Makefile.node` and `skills/jvm/templates/Makefile.gradle`. They run `npm test` and `npm run integration`, pack the dependencies for the next job, build and smoke-check the image, and release the JAR. They stay two files, because a language template includes `project.mk`, and `sdlc.mk` already defines `help`.

## Develop

`SDLC_OWN_CONTRACT` is removed from `sdlc.mk`, `container.mk`, `contract.mk`, the references, and the rows. `sdlc.mk` always includes `contract.mk` and `container.mk`.

Both templates set `SETUP_CMD`, `BUILD_CMD`, `TEST_CMD`, `FORMAT_CMD`, `FORMAT_FIX_CMD`, `LINT_CMD`, `INTEGRATION_CMD`, `COVERAGE_CMD`, `TEST_CHANGED_CMD`, `RENDER_DOCS`, `DOCS_CMD`, and `PUBLISH_IMAGE` above the include, and define none of the contract targets. A `#` in a command variable is written `\#`. The commands write `build/summaries/<job>.md` as before. The contract targets write no `build/logs/<job>.log`, because `SDLC_LOG` stays with the publish targets.

`container.mk` has three new variables: `IMAGE_CONTEXT`, `IMAGE_PREPARE`, and `PUBLISH_PREPARE`. The Gradle template builds the image from the tested JAR through them. The Node template ends `BUILD_CMD` with `make image-ci` and sets `IMAGE_BUILD_ARGS` and `SMOKE_CMD`.

`contract.mk` tests an empty `SETUP_CMD`, `BUILD_CMD`, and `DOCS_CMD` with `ifeq`, as it does for the other commands. The shell test `[ -z "$(BUILD_CMD)" ]` ran a command substitution inside the command variable once more and broke on a double quote.

Five unit tests in `test_project_report.py` read the templates, `contract.mk`, `container.mk`, and `sdlc.mk`. The test of the report names R-81 as its planned row, because R-79 is deleted. No test was weakened or deleted.

## Review

Gates run through Make in Podman: `make format`, `make lint`, `make test`, `make editorconfig`, `make ids`, `make toon`, and `make links-check`. A copy of each template ran in a scratch project with a stub `podman`, under Make 4.3 and under the image `localhost/make381`. `make -n` for each contract target gave the same commands in both, except that Make 3.81 keeps the tab of a continued line. The templates did not run against a real Node project or a real Gradle project.

Not run: `make integration` and `make coverage` have no entry in this repository. security: no listener and no secret. privacy: no personal data.

## Release

Not invoked: the owner merges this slice.
