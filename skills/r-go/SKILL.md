---
name: r-go
description: Go. Applies the Go rules to a change. Use when go is installed and the files in hand are Go. The stage skill still applies.
kind: language
files: [go]
names: [go.mod, go.sum]
stages: [r-develop]
---

The general rules in `CLAUDE.md` apply.

<purpose>
This skill gives the Make targets and the code rules for Go files.
</purpose>

<steps>
1. If the project is new or `go.mod` is missing, read `references/tooling.md`, then run `make go-tooling`.
2. Edit the Go files by the rules below.
3. If the program must run, run `make run ARGS='...'`.
4. If a one-off Go command is necessary, run `make go ARGS='...'`.
</steps>

<rules>
- `$(GO)` runs Go in Podman on this machine. `make setup` downloads the modules.
- The formatter is gofmt. The linter is `go vet`.
- `make format` lists the files that gofmt would change, and it fails when there is one.
- gofmt owns the layout of a Go file, so `.editorconfig` sets no indent rule for `*.go`.
- A test file is a file whose name ends with `_test.go`. Its `// id:` lines stand above the `package` line, with one blank line between.
- Go runs in a Linux container, so `build/<name>` is a Linux binary on every machine. Do not start that file on the host.
- A package has one job.
- An exported name has a doc comment.
- Return an error. Do not ignore it. Use `panic` only for an error that no caller can handle.
</rules>

<references>
- `references/tooling.md`: read it before `make go-tooling` runs, or when a Go cache volume is the question.
- `references/coverage.md`: read it when `make coverage`, `make test-changed`, `make format`, or `make run` fails.
- `references/build.md`: read it when the change touches `BIN`, `BIN_PKG`, `make build`, or a binary for another machine.
</references>
