<purpose>
This file gives the Go facts that `r-component-upgrade` needs. It adds no step.
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
