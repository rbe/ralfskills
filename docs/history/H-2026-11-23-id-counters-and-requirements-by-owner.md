---
id: H-2026-11-23-id-counters-and-requirements-by-owner
title: Repairs after the trials of the id counters and the requirement files
status: closed
adrs: [R-42, R-46, R-71, R-85, R-86]
skills: [develop, record, review, python, shell]
roadmap: []
proposals: []
---

# Repairs after the trials of the id counters and the requirement files

## Plan

The owner answered the open points of the earlier slices. The id counters of `docs/ids.yaml` replace the retired list, and no merged history exists, because only `record` reads `docs/ids.yaml`. An id is never reused. The requirement rows live in one file for each owning skill, and `make req` prints rows. The collection keeps no backward compatibility, because it has no users yet. The owner agreed to the removal of the planned row R-80. The planned row [R-81](../requirements/project-setup.md#r-81) stays, and the owner asked for a summary of it. The owner uses the repository `gh-sweep` for tests and takes care of the push on their own.

Five trials ran on copies and on a test repository: Covered by code, Node, Gradle, Go, and `gh-sweep`. The trials covered the pipeline templates, the makefiles, and the board skills. The owner chose no cover finding, so this slice applies none.

## Develop

Make now derives `NAME` once, in `skills/project-setup/tools.mk`: the repository name of the remote `origin`, else the directory name. The language templates of `go`, `node`, and `jvm` no longer set `NAME`, so the image name, the package label, and the tar name follow the remote.

`PACKAGE` in `sdlc.mk` defaults to `GITHUB_REPOSITORY`, else `OWNER/NAME`. `make ci` sets `JOB_RESULT_<JOB>=success` after each target, so the local report shows a result for each job. `container.mk` passes `PODMAN_NET_ARGS` to `podman build`. `podman-python.mk` adds `--userns=keep-id` on rootless Linux Podman, and the Node template uses it too.

The Gradle template of `github-pipeline` sets `INTEGRATION_CMD = true`, uses the same `LINT_CMD` as the `jvm` template, and passes `PODMAN_NET_ARGS` to Gradle. The `jvm` template passes it too. The Node and Gradle templates of `github-pipeline` leave `RENDER_DOCS` unset, set `SDLC_JOBS` and `SDLC_CI` without `docs`, and their workflows have no `docs` job. `templates/build.gradle` carries the commented `jar { manifest }` block, and `references/tooling.md` of `jvm` names it.

The Node language template runs `npm ci` before Prettier and ESLint when `node_modules` is missing. The three workflow templates are Prettier-clean. The Go `FORMAT_CMD` stops on a `gofmt` error. `Containerfile.go` is now `Containerfile.golang`. `Makefile.image` says to copy every line, says where `BUILD_CMD +=` stands, and names `node`. `references/setup-files.md` names the Gradle order, the Go layout, and the Node build script. `templates/pipeline-rules.md` has bracket placeholders in "This repository". `migrate-docs` deletes an old `docs/ids.yaml` with a `retired:` list first. `board-merge` says to commit one finding before the next edit. The rows [R-42](../requirements/github-pipeline.md#r-42), [R-46](../requirements/github-pipeline.md#r-46), and [R-71](../requirements/project-setup.md#r-71) say what the files now do.

The new planned rows are [R-85](../requirements/github-pipeline.md#r-85) (cleanup targets on a laptop) and [R-86](../requirements/board-merge-report.md#r-86) (size limit and test names of the cover finding), because each needs a decision of the owner.

## Review

Gates ran through Make in Podman after the last edit and passed: `make links`, `make format`, `make lint`, `make test` (125 tests), `make integration` (runs `true`), `make editorconfig`, `make coverage`, `make ids`, `make toon`, `make links-check`, `make project-report`, `make old-board`, and `make doctor`. No test changed.

Facts of the trials:
- Node: a fresh checkout failed `make lint`, `make format` failed on the unformatted workflow template, and the image name followed the directory name.
- Gradle: `make integration` called a task that no skill defines, `make docs` called a script that no skill ships, and `java -jar` found no main manifest.
- Go: the image name followed the directory name, and the Containerfile template had a name that ends in `.go`.
- `gh-sweep`: CI failed on rootless Podman with a permission error, `PACKAGE` was empty on a laptop, and a pull request merged into a test branch with a green CI run.
- Covered by code: 16 rows have facts that tests pin. Two copy edits cut 256 words. The cover findings are not applied here.
- `make ci` in a scratch repository with the remote `https://github.com/acme/hello.git` printed the image name `ghcr.io/acme/hello` and a result `success` for `setup`, `build`, and `test`. GNU Make 3.81 ran `make -n image` there.
- Not defects: a raise of a counter to its own value fails by design, a Podman volume deadlock came from the container of the trial, `make help` lists `py` because the board targets run Python, and the `Diff:` line of `make coverage` is output of diff-cover.
- security, privacy, ux-ui-design, api-design: not touched.

Not run: a real GitHub Actions run of the changed templates, `apm install`, `make publish-container`, `make publish-github`, the cleanup targets, `npm ci` and Prettier on the changed Node template, Gradle on the changed Gradle templates, `go` on the changed Go template, and the rootless `--userns=keep-id` path on a Linux runner.

## Release

Not invoked: the owner merges and pushes this slice.
