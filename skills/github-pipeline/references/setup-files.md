# Files of setup mode and report mode

A path that starts with `templates/`, and `sdlc.mk` and `container.mk`, are files of this skill. Every other path is a file of the project.

## Files to read

| File | Use |
| --- | --- |
| `sdlc.mk` | The makefile that the project includes |
| `container.mk` | The image targets of a project that has no recipe of its own for them. `sdlc.mk` includes it |
| `templates/Makefile.node`, `templates/ci.node.yml` | Node toolchain. A Node app, image only. Node 24 is the toolchain of this template only |
| `templates/Makefile.gradle`, `templates/ci.gradle.yml` | Gradle toolchain. A Gradle app, image plus a JAR release. The JDK image in the template is its toolchain |
| `templates/ci.make.yml`, `templates/Makefile.image` | The workflow and the image block of a project on the Makefile of its language skill: Python, Go, or another language |
| `templates/Containerfile.node`, `templates/Containerfile.gradle`, `templates/Containerfile.python`, `templates/Containerfile.go` | The source of `Containerfile`, by toolchain |
| `templates/pipeline-rules.md` | The source of `docs/pipeline-rules.md` |
| `templates/containerignore`, `templates/gitignore` | The source of `.containerignore` and `.gitignore` |
| `templates/contract-report.md` | The skeleton of report mode |
| `Makefile`, `.github/workflows/`, `docs/pipeline-rules.md`, `Containerfile`, `.containerignore`, `.gitignore` | The project, when present |

The Node template and the Gradle template are for a project that has no language Makefile of its own. They have the placeholder lines `NAME ?= app` and `OWNER ?= owner`. Replace both values with the name and the owner of the repository. A project diverges from a template only when it has a different output or toolchain, and it writes that down as a divergence.

## The include switch

If the Makefile includes `project.mk` or `.claude/skills/project-setup/project.mk`, do these steps:

1. Change the include to `.claude/skills/github-pipeline/sdlc.mk`.
2. Remove the `project.mk` include.

`sdlc.mk` provides `help`, and it includes `contract.mk`, the contract targets of `project-setup`: `setup`, `build`, `test`, `format`, `lint`, `coverage`, and the others. The command variables of the language Makefile therefore keep their effect.

If a project has no `project.mk` include and writes its own recipes for those targets, it sets `SDLC_OWN_CONTRACT = 1` before the include. The Node template and the Gradle template do this today. That is an exception to the rule of `project-setup`, which keeps the contract targets in `contract.mk` and changes them only through the command variables.
## The image block of a language Makefile

A project on the Makefile of the `python` skill or the `go` skill does these steps:

1. Take the image block of `templates/Makefile.image`.
2. Leave `OWNER` and `NAME` unset. They default to the owner and the repository name in `git remote get-url origin`. Set them only if the project has no remote or has another name.
3. Copy the `Containerfile` template of the language. Change `PACKAGE` or `NAME` in it.
4. Use `templates/ci.make.yml` as `.github/workflows/ci.yml`.

`make build` then builds the image, runs the smoke check, and saves the image tar.

## What the image and the repository contain

- The image copies named files, not the work tree.
- `templates/containerignore` is the list of paths that `.containerignore` keeps out of the image build. The list is `.git`, `.github`, `.claude/`, `apm_modules/`, `CLAUDE.md`, `docs/`, `build/`, `node_modules`, `data/`, `.env`, `.env.*`, and `*.tar`.
- `.claude/skills/` is committed, because Make includes files from it. The image still excludes `.claude/`.
- `templates/gitignore` is the list of paths that `.gitignore` keeps out of Git: build output, image tars, `data/`, and `.env`.
