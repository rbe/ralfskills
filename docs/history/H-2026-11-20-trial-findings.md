---
id: H-2026-11-20-trial-findings
title: Fix what two trial projects found
status: closed
adrs: []
skills: [plan, develop, review, release, record, project-report, project-setup, github-pipeline, node, python, shell, security, migrate-docs]
decisions: [D-9]
proposals: []
issues: []
---

# Fix what two trial projects found

## Plan

`plan` was not invoked. Two agents used the collection as a project does. One set up a new Node project. One onboarded an existing Python project that had an old board. Each installed the skills with APM, followed only the installed skills, and delivered one change to a local remote. Both delivered the change, and both said an agent cannot do it with the skills alone. Their findings are the input of this slice.

Boundary: `record` owns the layout of each board document. Each language skill owns the Makefile of its language. `project-setup` owns the setup of a project that has no toolchain yet. `release` owns the order of the close, the commit, and the merge.

Pattern: what an agent had to guess is now a template or a numbered step.

## Develop

A test names an ADR or a decision. It does not name a roadmap line or a known issue. Those ids are retired when the work ends, and the project report then failed. D-9 records the choice. The report reads a decision and a known issue as table rows.

`record` has a template for each board document. A decision and a known issue are table rows. `record` adds the roadmap line when it creates a history file.

`python` has a Makefile template and a `.coveragerc` template. `node` has a Makefile template, a `.prettierignore` template, and an ESLint config template. `$(NODE)` runs Node and npm in Podman, and `make npm` creates the manifest. `project-setup` copies the templates for a new project.

`release` writes the Release section and asks for the close before the commit. A library package is a shipment.

`make format` checks. `make format-fix` rewrites. The coverage recipes mark a new file with `git add -N`, and they work in a repository with no commit. The README `apm.yml` has `name` and `version`.

`migrate-docs` and `record` name the id check for a project whose Makefile has no include yet. `security` asks for the bound on each input. A request that names a known issue starts at `develop`.

Python and shell are the language skills.

## Review

Every gate passed through Make in Podman: `make format`, `make lint`, `make test`, `make integration`, `make editorconfig`, `make coverage`, `make test-changed`, `make ids`, `make toon`, `make project-report`, and `make decision-log`. The diff report shows every changed line covered. The Python images came from `mirror.gcr.io`, because Docker Hub refused the pull.

The Node template created a project through `make npm` and passed every target in Podman, in a repository with no commit. The Python template passed every target in Podman. Jest and Vitest passed with the pipeline template in Podman.

security: no listener, no secret, no personal data in a fixture. A template contains no credential.

privacy: no personal data.

ux-ui-design: no screen.

api-design: not HTTP. Not a module export. The layouts of the board documents are the interface between `record` and the scripts.

No finding. Left alone: the two reviews in the project report are lists, not a judgement, and the skill says so. A JVM project on `project.mk` has no Makefile template. The pipeline template for Gradle is the example.

## Release

The branch is pushed and merged into the default branch with a pull request, after the owner confirmed. This collection publishes no image.
