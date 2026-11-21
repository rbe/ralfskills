# Shared makefile for the Make contract. A project includes this file
# from the installed skill and does not keep a second copy at the root.
#
#     SETUP_CMD = npm ci
#     BUILD_CMD = npm run build
#     TEST_CMD = npm test
#     include .claude/skills/project-setup/project.mk
#
# Set RENDER_DOCS=1 when the repository renders docs, and
# PUBLISH_IMAGE=1 when it publishes an image. Those targets are
# absent otherwise. login is the registry login. build, test, and
# docs are stubs: an empty command fails the target and names the
# variable to set.
#
# GNU Make 3.81, including the macOS system make. Recipes do not use the
# one-shell option or Make 4 functions. Each recipe is one shell, joined
# with backslashes, and does not depend on shell flags from the makefile.
# The shell is POSIX sh. There is no shell-script wrapper. A shell `$`
# in a command variable is `$$`.
#
# help is the default goal, set again after the included fragments.
# It lists every target in this file that has
# a ## comment. docs and login are listed only when that target exists.
# The `# help-docs` and `# help-login` markers are how help knows.
#
# setup installs jq through Homebrew when brew is on PATH, then any
# names in BREW_TOOLS, then runs SETUP_CMD. A tool already on PATH is
# left in place. When brew is missing, setup prints `brew install` and
# the tool names, then continues if those tools are already on PATH.
# A missing tool and no Homebrew fails setup before SETUP_CMD.
#
# Set before the include:
#   HELP_LEAD        first line of `make help`
#   BREW_TOOLS       extra tools setup installs. jq is always included
#   SETUP_CMD        how this project resolves dependencies
#   BUILD_CMD        how this project produces the artifact
#   TEST_CMD         how this project runs the unit tests
#   FORMAT_CMD       the one formatter. The language skill names the tool
#   FORMAT_FIX_CMD   the same formatter in write mode, for make format-fix
#   LINT_CMD         the one linter. The language skill names the tool
#   INTEGRATION_CMD  the one integration entry
#   COVERAGE_CMD     writes build/coverage/diff.md and the map test-changed reads
#   TEST_CHANGED_CMD tests that cover the diff, selected from that map
#   PROJECT_REPORT_CMD writes build/project-report.md
#   RENDER_DOCS      1 when this repository renders docs
#   DOCS_CMD         the renderer, required when RENDER_DOCS is 1
#   PUBLISH_IMAGE    1 when an image is published
#   REGISTRY         login host. Default ghcr.io

ifndef PROJECT_MK
PROJECT_MK := 1

PROJECT_MK_DIR := $(dir $(lastword $(MAKEFILE_LIST)))
include $(PROJECT_MK_DIR)podman-python.mk
include $(PROJECT_MK_DIR)tools.mk
include $(PROJECT_MK_DIR)doctor.mk
include $(PROJECT_MK_DIR)test-changed.mk
-include .claude/skills/project-report/report.mk

HELP_LEAD ?= Make is the only interface. A target does the same thing locally and in CI.

.PHONY: help

help: ## Show the targets
	@printf '%s\n' "$(HELP_LEAD)"
	@printf '%s\n' ""
	@awk -v docs="$(RENDER_DOCS)" -v login="$(PUBLISH_IMAGE)" 'BEGIN {FS = ":.*## "}; /^# help-docs$$/ { skip = (docs != "1"); next } /^# help-login$$/ { skip = (login != "1"); next } /^endif$$/ { skip = 0; next } skip { next } /^[a-zA-Z][a-zA-Z0-9_-]*:.*## / && !seen[$$1]++ {printf "  %-32s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

# The targets of the Make contract: setup, build, test, editorconfig,
# format, format-fix, lint, integration, coverage, project-report, and,
# when the variables say so, docs and login. sdlc.mk includes the same
# file, so a project on either include has them.
include $(PROJECT_MK_DIR)contract.mk

-include .claude/skills/record/index.mk

# After the fragments this file includes. A fragment must not replace it.
.DEFAULT_GOAL := help

endif
