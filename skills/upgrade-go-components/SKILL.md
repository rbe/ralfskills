---
name: upgrade-go-components
description: "Gives the Go facts for component-upgrade: where each version is pinned, which target changes the lock file, and the known traps. Use with component-upgrade when the component is the Go toolchain, a Go module, or a Go base image."
---

The general rules in `CLAUDE.md` apply.

<purpose>
This skill gives the Go facts that `component-upgrade` needs. It adds no step.
</purpose>

<rules>
- The Go toolchain is `GO_IMAGE` in the Makefile. Every recipe runs in it.
- The base image of the build stage is the `ARG GO_IMAGE` default in the Containerfile. The Makefile passes `GO_IMAGE` to it when `IMAGE_BUILD_ARGS` is set.
- A module is in `go.mod`. `go.sum` holds its checksums.
- To change a module or the checksums, run `make go ARGS='...'`.
- `make setup` runs `go mod download`. It does not change `go.mod`.
- A change of the Go version changes `GO_IMAGE` and the Containerfile default in the same slice.
- The final image is `scratch`. It has no operating system pin to change.
</rules>
