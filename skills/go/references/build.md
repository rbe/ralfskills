# Go build

## `BIN` and `make build`

- A project that ships a binary sets `BIN` to the name of the binary, in the first line of the Makefile.
- `project-setup` sets `BIN` in setup mode, after the owner said how the project ships.
- With `BIN` set, `make build` writes `build/<name>` from the package `./cmd/<name>`.
- `BIN_PKG` names a different package. An example is `.` when the root is the main package.
- With `BIN` empty, `make build` compiles every package and writes no file. A library uses this.

## Binary for another machine

`make build GOOS=darwin GOARCH=arm64` writes the binary of another machine.
