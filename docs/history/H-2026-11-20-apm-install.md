---
id: H-2026-11-20-apm-install
title: Make the collection install with APM and select changed tests in Node and the JVM
status: closed
adrs: []
skills: [develop, review, record, project-report, project-setup, github-pipeline, node, jvm, python, shell]
decisions: []
proposals: []
issues: []
---

# Make the collection install with APM and select changed tests in Node and the JVM

## Plan

`plan` was not invoked. The gaps were named after the previous slice: the APM install was not tested, a Node or JVM project had no selection of changed tests, and no Containerfile template existed.

Boundary: `record` owns the frontmatter check in `make toon`. `project-report` owns the coverage map scripts. `github-pipeline` owns the container templates and the Makefile templates.

Pattern: a coverage map is one JSON file, test to files, for every language. A script for each language writes it. One script reads it.

## Develop

APM 0.36.1 refused to install the collection. The descriptions of `security`, `privacy`, `ux-ui-design`, and `api-design` had a colon followed by a space, which is not one YAML string. The descriptions are changed. `make toon` fails on that defect. [R-65](../REQUIREMENTS.md#r-65) states the rule.

The project report read the tests in `apm_modules/`, the copy APM keeps. It skips that directory now.

`node_cover_map.py` writes the coverage map from V8 coverage files. `jacoco_cover_map.py` writes it from the JaCoCo execution data. `changed_tests.py --print` names the chosen tests. The Makefile templates for Node and Gradle set `TEST_CHANGED_CMD` and write the map in `coverage`.

`github-pipeline` has the templates `Containerfile.node`, `Containerfile.gradle`, `containerignore`, and `gitignore`.

Python and shell are the language skills.

## Review

`make test`, `make integration`, `make lint`, `make format`, `make editorconfig`, `make ids`, `make toon`, `make project-report`, `make decision-log`, and `make test-changed` passed in Podman with the pinned images. `PYTHON_IMAGE` was the same image from `mirror.gcr.io`, because Docker Hub refused the pull. In `make coverage`, the tests and the coverage map passed in Podman. The diff-cover step did not run in Podman: its container installs git over plain HTTP, and the network of this machine refuses plain HTTP. diff-cover 11.0.2 wrote `build/coverage/diff.md` on the host.

APM installed nine skills from this branch into a sample project. `make toon`, `make ids`, `make project-report`, and `make decision-log` ran there. `apm compile` kept a `CLAUDE.md` that a person wrote.

The Node template ran in Podman in a sample project: `make coverage` wrote the map, and `make test-changed` ran the one test that covers the changed file. The Gradle template did the same with the Gradle on this machine and a real JaCoCo file. Both Containerfile templates built in Podman.

security: the image templates run as a user that is not root. `.containerignore` keeps `.env` out of the image. No secret in a fixture.

privacy: no personal data.

ux-ui-design: no screen.

api-design: not HTTP. Not a module export. `covered.json` is the one interface between the map scripts and the selection.

No finding. Left alone: a test runner that shares one process between test files makes the Node map coarser. That was not tried with Jest or Vitest. The Gradle template was not run in its JDK image. The remote branch of the previous slice cannot be deleted from this machine.

## Release

The branch is pushed and merged into the default branch with a pull request, after the owner confirmed. This collection publishes no image.
