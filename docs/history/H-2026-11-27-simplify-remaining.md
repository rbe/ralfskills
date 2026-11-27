---
id: H-2026-11-27-simplify-remaining
title: The last ten findings of the simplification review
status: started
adrs: [R-11, R-60, R-104, R-111, R-125, R-126]
skills: [plan, develop, review, record]
roadmap: []
proposals: []
---

# The last ten findings of the simplification review

## Plan

The owner answered twelve questions on findings 6, 8, 9, 10, 11, 12, 13, 15, 16 and 17 of the simplification review of 2026-11-26. `sdlc.mk` includes `project.mk` once. One CI template `ci.yml` replaces three. Node and Gradle use their language template plus `Makefile.image`. The four upgrade skills become `references/upgrade.md` of the language skills. The README links the skill folders. `check-docs` skips targets of skills that are not installed. Closed history files are shortened to 150 words. One renderer replaces the project renderers ([R-125](../requirements/project-setup.md#r-125)). Published images cover two platforms ([R-126](../requirements/github-pipeline.md#r-126)).

## Develop

Five agents changed separate files. `sdlc.mk` includes `project.mk`, which owns `help`; `HELP_NOTES` adds the two lines of `sdlc.mk`. `container.mk` has `PLATFORMS` and `multiarch-host`. `templates/ci.yml` has marked blocks for Node, Image, JAR, and Release. `Makefile.image` has Node, JAR, and Release blocks. `scripts/render_docs.py` of `r-project-setup` is the default `DOCS_CMD`, with `DOCS_OPTIONS`. 42 closed history files were shortened, and `H-2026-11-22-one-list-for-rules` is closed.

## Review

After the last edit, `make toon`, `links`, `ids`, `links-check`, `check-docs`, `editorconfig`, `format`, `lint`, `test` (246 tests), `integration`, and `coverage` (99% of 541 changed lines) passed. They ran in a cloud container with Docker behind a `podman` shim. Not run: a real two-platform build and push, because the container has no binfmt support.

## Release

Not invoked yet.
