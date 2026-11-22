# Go tooling

## `make go-tooling`

`make go-tooling` sets up a new Go project. It does these things in order:

1. If `go.mod` is missing, it runs `go mod init` with `MODULE`. The default of `MODULE` is `example.com/<directory>`. `make go-tooling MODULE=github.com/acme/app` sets a different module path.
2. It adds `build/` and `bin/` to `.gitignore`.
3. If the project has a Go package, it runs `make format-fix`.

## Go caches

The Go caches are two container volumes. Their names come from the project directory. Two projects on one machine do not share a volume.
