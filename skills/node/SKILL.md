---
name: node
description: Node and TypeScript. Use when node is installed and the files in hand are JavaScript or TypeScript. Tests and installs run through make. A framework named in CLAUDE.md is a reference file beside this skill. The stage skill still applies.
kind: language
files: [js, jsx, ts, tsx, mjs, cjs]
---

# Node

## Steps

1. If `docs/BUGS.md`, `docs/WAVES.md`, `docs/FEATURES.md`, `docs/bugs/`, `docs/waves/`, or `docs/features/` exists, stop. Name `migrate-docs`. Do not take a later step.
2. Invoke `record` before creating an id or a document. A write that skips `record` fails this step.
3. Do the work below. `develop` invokes this skill for JavaScript and TypeScript files.
4. Ask `record` to add one line under Develop naming `node`. Do not open a second history file.

## Work

1. `make test` runs the tests. `make setup` installs dependencies. Do not run the package manager from a workflow step. `templates/Makefile.node` beside this skill is the Makefile of a Node project on `project.mk`: `$(NODE)` runs Node and npm in Podman, and each command variable is filled in for `node --test`, Prettier, and ESLint. `make npm ARGS='...'` runs npm in Podman. Use it to create `package.json` and to add a dependency. Do not run npm on the host. `templates/prettierignore` and `templates/eslint.config.mjs` are the files those tools need. `project-setup` copies them to `.prettierignore` and `eslint.config.mjs`. `.gitignore` has the lines `node_modules/` and `coverage/`. After `npm init`, set the name, the version, and `type=module` with `make npm ARGS='pkg set ...'`. A library sets `exports` and `files` in `package.json`, so `make build` packs the source and nothing else. Source is in `src/`. The comment at the top of the template has each command.
2. The formatter is Prettier. The linter is ESLint, including for TypeScript. Do not write a linter. Do not add a second formatter or a second linter.
3. `make coverage` runs the test runner's lcov or Cobertura output through diff-cover. The report is the lines this change touched. Do not use a repository-wide percentage. `make coverage` also runs the tests with `NODE_V8_COVERAGE` set to `build/coverage/v8`, then `node_cover_map.py` from `project-report`. That script writes the coverage map: each test file, and the project files that ran in its process. `make test-changed` gives the test files that `changed_tests.py --print` names to the test runner. The map is exact with `node --test` and with Jest. A runner that shares a process between test files selects more tests, never fewer. The workers of Vitest write no V8 coverage. A Vitest project leaves the map step out of `coverage` and sets `TEST_CHANGED_CMD` to `vitest related --run` with the files in `build/coverage/changed.txt`. Vitest then selects the tests from its module graph. Record that choice as a Decided entry through `record`.
4. The language is TypeScript when the project already uses it. A new file follows that choice.
5. When `CLAUDE.md` names a framework, read `references/` beside this skill for that name. The framework file does not replace this skill or the stage skill.
6. Podman, XDG paths, and what a shipment may contain are `project-setup`.
