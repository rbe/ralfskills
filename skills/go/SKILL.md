---
name: go
description: Go. Use when go is installed and the files in hand are Go. Go runs in Podman through make. gofmt is the formatter and go vet is the linter. The stage skill still applies.
kind: language
files: [go]
names: [go.mod, go.sum]
---

# Go

## Steps

1. If `docs/BUGS.md`, `docs/WAVES.md`, `docs/FEATURES.md`, `docs/bugs/`, `docs/waves/`, or `docs/features/` exists, stop. Name `migrate-docs`. Do not take a later step.
2. Invoke `record` before creating an id or a document. A write that skips `record` fails this step.
3. Do the work below. `develop` invokes this skill for Go files.
4. Ask `record` to add one line under Develop naming `go`. Do not open a second history file.

## Work

1. Do not run `go` or `gofmt` on the host. `$(GO)` runs Go in Podman on this machine. `make test` runs the tests. `make setup` downloads the modules. A Makefile from the template has `make go ARGS='...'` for a one-off command, such as `make go ARGS='mod init example.com/name'` for a new project. A project that keeps its own Makefile may have no such target. CI runs the same targets.
2. `templates/Makefile.golang` beside this skill is the Makefile of a Go project on `project.mk`: each command variable, with gofmt, go vet, the coverage report, and the changed tests. `project-setup` copies it to `Makefile`. The Go caches are two container volumes named after the project directory, so two projects on one machine do not share a volume. `make build` compiles every package and writes no file. A project that ships a binary sets `BUILD_CMD` to the command that writes it. Do not write these commands again from memory. `.gitignore` has the lines `build/` and `bin/`.
3. The formatter is gofmt. `make format` lists the files gofmt would change and fails when there is one. gofmt reads the Go files of the packages of the project. It does not read `.claude/`. `make format-fix` rewrites them. The linter is `go vet`. gofmt owns the layout of a Go file, so `.editorconfig` sets no indent rule for `*.go`. Do not write a linter. Do not add a second formatter or a second linter.
4. `make coverage` runs the tests of each package with a cover profile. `go_cover_map.py` from `project-report` reads the profiles. It writes the Cobertura file that diff-cover reads and the coverage map: each package with tests, and the Go files those tests ran. The report is the lines this change touched. Do not use a repository-wide percentage.
5. `make test-changed` gives the packages that `changed_tests.py --print` names to `go test`. The unit of selection is the package.
6. A test file names its requirement in a comment in the file header: `// id: D-1`, one line for each id. The lines are above the `package` line, with one blank line between them and it. A test file is a file whose name ends with `_test.go`.
7. A package has one job. An exported name has a doc comment. An error is returned, not ignored. Do not use `panic` for an error a caller can handle.
8. Podman, XDG paths, and what a shipment may contain are `project-setup`.
