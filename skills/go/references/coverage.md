# Coverage, changed tests, format, and run in a Go project

## `make coverage`

- `make coverage` runs the tests of each package with a cover profile.
- `go_cover_map.py` from `project-report` reads the profiles.
- That script writes the Cobertura file that diff-cover reads, and the coverage map: each package with tests, and the Go files that those tests ran.

## `make test-changed`

- `make test-changed` selects by package.
- It gives the packages that `changed_tests.py --print` names to `go test`.

## `make format`

- gofmt reads the Go files of the packages of the project. It does not read `.claude/`.

## `make run`

- `make run` compiles the package and does not read `build/`.
- A program with a screen needs a terminal. If Make has a terminal, `make run` gives the program a terminal.
