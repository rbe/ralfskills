# Requirements of node

The rows that the skill `node` owns. `collection.md` says what the status means.

| Id | Title | Status | Statement |
| --- | --- | --- | --- |
| <a id="r-36"></a>R-36 | Node and TypeScript | in force | `node` applies when it is installed and the files are JavaScript or TypeScript. Its `files` are `js`, `jsx`, `ts`, `tsx`, `mjs`, and `cjs`. `make test` runs the tests. `make setup` installs dependencies. A workflow step does not run the package manager. The formatter is Prettier. The linter is ESLint. The language is TypeScript when the project already uses it, and a new file follows that choice. `make coverage` runs the test runner's lcov or Cobertura output through diff-cover. When `CLAUDE.md` names a framework, read `references/` beside this skill for that name. Express, React, and Vite have no reference file yet, and they do not get a second lifecycle. Podman, XDG paths, and shipment contents stay in `project-setup`. This applies to a product repository that installs `node`. `node` owns these rules. |
