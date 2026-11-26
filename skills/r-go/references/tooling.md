# Go tooling

## `make go-tooling`

`go.mk` beside this skill has the targets `go` and `go-tooling`, and the defaults of `GO_IMAGE`, `GO_CACHE`, `GO_OPTS`, `GO_RUN`, `GO`, and `MODULE`. The Makefile includes it with `include .claude/skills/r-go/go.mk` after `project.mk` or `sdlc.mk`. To change a variable, set it before that include.

`make go-tooling` sets up a new Go project. It does these things in order:

1. If `go.mod` is missing, it runs `go mod init` with `MODULE`. The default of `MODULE` is `example.com/<directory>`. `make go-tooling MODULE=github.com/acme/app` sets a different module path.
2. It adds `build/` and `bin/` to `.gitignore`.
3. If the project has a Go package, it runs `make format-fix`.

## Go caches

The Go caches are two container volumes. Their names come from the project directory. Two projects on one machine do not share a volume.
