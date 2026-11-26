---
name: r-upgrade-python-components
description: "Gives the Python facts for r-component-upgrade: where each version is pinned, which target changes the lock file, and the known traps. Use with r-component-upgrade when the component is the Python runtime, a Python package, a Python base image, or the Ruff or coverage pin."
---

The general rules in `CLAUDE.md` apply.

<purpose>
This skill gives the Python facts that `r-component-upgrade` needs. It adds no step.
</purpose>

<rules>
- The Python runtime of every recipe is `PYTHON_IMAGE`. Set it in the Makefile before the include. `r-project-setup` gives the default.
- The base image of the app is the `ARG PYTHON_IMAGE` default in the Containerfile. The Makefile passes `PYTHON_IMAGE` to it when `IMAGE_BUILD_ARGS` is set.
- The formatter and linter pin is `RUFF_IMAGE`. The coverage pins are `COVERAGE_VERSION`, `DIFF_COVER_VERSION`, and `DIFF_COVER_IMAGE`. `tools.mk` of `r-project-setup` gives their defaults.
- The Makefile template has no target that resolves dependencies or writes a lock file. `SETUP_CMD` is `true`.
- If the project keeps a requirements file, the Containerfile installs it. Change that file and the pin in one slice.
- A change of the Python version changes `PYTHON_IMAGE` and the Containerfile default in the same slice. `DIFF_COVER_IMAGE` is a separate pin.
- `make coverage` installs `coverage` with `pip` at the pinned `COVERAGE_VERSION`. A new `coverage` version changes that variable.
</rules>
