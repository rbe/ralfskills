---
id: H-2026-11-21-node-tooling
title: make node-tooling sets up the Node tooling in one run
status: closed
adrs: []
skills: [develop, review, record, project-setup, node, shell]
decisions: []
proposals: []
issues: []
---

# make node-tooling sets up the Node tooling in one run

## Plan

`plan` was not invoked. The owner gave the target text for the Node template.

Boundary: `node` owns its Makefile template. `project-setup` owns the order of setup mode.

Pattern: what an agent had to do in five `make npm` calls is one Make target.

## Develop

The Node template has the target `node-tooling`. It creates `package.json` when it is missing, adds the dev tools as exact versions, writes the config files when they are missing, adds the `.gitignore` lines, and runs `make format-fix`.

The owner's text is changed in four places, because the template differs from the Makefile it came from. The template calls Node `$(NODE)`, so each `$(NODE_RUN)` is `$(NODE)`. `$(THIS_MAKE)` is `$(MAKE)`. `project.mk` already defines `editorconfig`, `format`, `format-fix`, `lint`, `integration`, and `coverage`, and the template has `npm` already, so those targets are not copied. The template has no `deps` target, because `make setup` runs `npm ci` and `node-tooling` installs the tools itself.

The template sets `NAME` and `NODE_DEV_TOOLS` with `?=`. `NAME` is the name of the directory. The target also runs `npm pkg delete main repository scripts` after `npm init`, as the old comment of the template did, and it adds `node_modules/` and `coverage/` to `.gitignore`.

`node` and `project-setup` name the target. [R-66](../requirements/collection.md#r-66) states it.

Shell is the language skill.

## Review

Every gate passed through Make in Podman with the pinned default images: `make format`, `make lint`, `make test`, `make integration`, `make editorconfig`, `make coverage`, `make test-changed`, `make ids`, `make toon`, `make links-check`, `make project-report`, and `make decision-log`.

The target ran in a new directory with the template and the installed skills. It created `package.json`, installed four tools, and wrote `.prettierignore`, `eslint.config.mjs`, `.editorconfig`, and `.gitignore`. Then `make format`, `make lint`, and `make editorconfig` passed. A second run changed no file and printed that the tools were already there. After `package.json` was deleted, a run created it again.

security: the target runs npm in Podman and installs the four named packages from the npm registry. No listener, no secret. A package version is exact, and `package-lock.json` pins the tree.

privacy: no personal data.

ux-ui-design: no screen.

api-design: not HTTP. Not a module export. `NAME` and `NODE_DEV_TOOLS` are the interface of the target.

No finding. Left alone: a project that keeps Jest or Vitest has no test runner step here. The target sets up the formatter and the linter only. A trial agent did not use the target. A project with an old `package.json` that already has the tools was tested only by the second run.

## Release

The branch is pushed and merged into the default branch with a pull request, after the owner confirmed. This collection publishes no image.
