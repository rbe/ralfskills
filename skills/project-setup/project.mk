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

HELP_LEAD ?= Make is the only interface. A target does the same thing locally and in CI.
REGISTRY ?= ghcr.io

.PHONY: help setup build test test-changed project-report editorconfig format lint integration coverage

help: ## Show the targets
	@printf '%s\n' "$(HELP_LEAD)"
	@printf '%s\n' ""
	@awk -v docs="$(RENDER_DOCS)" -v login="$(PUBLISH_IMAGE)" 'BEGIN {FS = ":.*## "}; /^# help-docs$$/ { skip = (docs != "1"); next } /^# help-login$$/ { skip = (login != "1"); next } /^endif$$/ { skip = 0; next } skip { next } /^[a-zA-Z][a-zA-Z0-9_-]*:.*## / {printf "  %-32s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

# Real recipe for the tools every project shares, then the project stub.
setup: ## Resolve dependencies
	@set -eu; \
	tools="jq $(BREW_TOOLS)"; \
	list=""; \
	for tool in $$tools; do \
	  if [ -z "$$tool" ]; then continue; fi; \
	  case " $$list " in \
	    *" $$tool "*) continue ;; \
	  esac; \
	  if [ -z "$$list" ]; then list="$$tool"; else list="$$list $$tool"; fi; \
	done; \
	if command -v brew >/dev/null 2>&1; then \
	  for tool in $$list; do \
	    if ! command -v "$$tool" >/dev/null 2>&1; then brew install "$$tool"; fi; \
	  done; \
	else \
	  printf '%s\n' "Homebrew is not on PATH. Install standard tools with: brew install $$list" >&2; \
	  for tool in $$list; do \
	    if ! command -v "$$tool" >/dev/null 2>&1; then \
	      printf '%s\n' "Missing $$tool." >&2; \
	      exit 1; \
	    fi; \
	  done; \
	fi; \
	if [ -z "$(SETUP_CMD)" ]; then \
	  printf '%s\n' "setup: stub. Set SETUP_CMD before the include. Resolve this project's dependencies." >&2; \
	  exit 1; \
	fi; \
	$(SETUP_CMD)

# Stub. The project sets BUILD_CMD. Empty fails the target.
build: ## Produce the artifact
	@set -eu; \
	if [ -z "$(BUILD_CMD)" ]; then \
	  printf '%s\n' "build: stub. Set BUILD_CMD before the include. Produce this project's artifact." >&2; \
	  exit 1; \
	fi; \
	$(BUILD_CMD)

# Stub. The project sets TEST_CMD. Empty fails the target.
# test is the unit tests. integration is the one integration entry.
test: ## Run the unit tests
ifeq ($(strip $(TEST_CMD)),)
	@printf '%s\n' "test: stub. Set TEST_CMD before the include. Run this project's unit tests." >&2
	@exit 1
else
	$(TEST_CMD)
endif

editorconfig: ## Check files against .editorconfig
	$(EDITORCONFIG)

format: ## Run the one formatter
ifeq ($(strip $(FORMAT_CMD)),)
	@printf '%s\n' "format: stub. Set FORMAT_CMD before the include. One existing formatter." >&2
	@exit 1
else
	$(FORMAT_CMD)
endif

lint: ## Run the one linter
ifeq ($(strip $(LINT_CMD)),)
	@printf '%s\n' "lint: stub. Set LINT_CMD before the include. One existing linter." >&2
	@exit 1
else
	$(LINT_CMD)
endif

integration: ## Run the one integration entry
ifeq ($(strip $(INTEGRATION_CMD)),)
	@printf '%s\n' "integration: stub. Set INTEGRATION_CMD before the include. One integration entry." >&2
	@exit 1
else
	$(INTEGRATION_CMD)
endif

# COVERAGE_CMD writes build/coverage/diff.md. diff-cover is DIFF_COVER in tools.mk.
coverage: ## Report the lines this change touched
ifeq ($(strip $(COVERAGE_CMD)),)
	@printf '%s\n' "coverage: stub. Set COVERAGE_CMD before the include. Write build/coverage/diff.md for the lines this change touched." >&2
	@exit 1
else
	mkdir -p build/coverage
	$(COVERAGE_CMD)
endif

# Tests whose coverage includes a file in the diff. Not a CI substitute for test.
test-changed: ## Run the tests that cover the diff
ifeq ($(strip $(TEST_CHANGED_CMD)),)
	@printf '%s\n' "test-changed: stub. Set TEST_CHANGED_CMD before the include. Select tests from coverage of the files in the diff." >&2
	@exit 1
else
	@set -eu; \
	mkdir -p build/coverage; \
	base=$$(git merge-base HEAD origin/main 2>/dev/null || printf '%s' HEAD); \
	git diff --name-only "$$base" > build/coverage/changed.txt; \
	git diff --name-only >> build/coverage/changed.txt; \
	git diff --name-only --cached >> build/coverage/changed.txt; \
	git ls-files --others --exclude-standard >> build/coverage/changed.txt; \
	sort -u build/coverage/changed.txt -o build/coverage/changed.txt; \
	$(TEST_CHANGED_CMD)
endif

# Generated. Hand-editing build/project-report.md is a defect.
project-report: ## Write the requirements map and the reviews
ifeq ($(strip $(PROJECT_REPORT_CMD)),)
	@printf '%s\n' "project-report: stub. Set PROJECT_REPORT_CMD before the include. Write build/project-report.md." >&2
	@exit 1
else
	mkdir -p build
	$(PROJECT_REPORT_CMD) > build/project-report.md
endif

# Stub. Set RENDER_DOCS=1 only when this repository renders docs.
# Marker `# help-docs`: help lists this target only when RENDER_DOCS is 1.
ifeq ($(RENDER_DOCS),1)
# help-docs
.PHONY: docs
docs: ## Render the docs
	@set -eu; \
	if [ -z "$(DOCS_CMD)" ]; then \
	  printf '%s\n' "docs: stub. Set DOCS_CMD before the include. Run this project's renderer." >&2; \
	  exit 1; \
	fi; \
	$(DOCS_CMD)
endif

# Real recipe. Set PUBLISH_IMAGE=1 only when an image is published.
# Marker `# help-login`: help lists this target only when PUBLISH_IMAGE is 1.
ifeq ($(PUBLISH_IMAGE),1)
# help-login
.PHONY: login
login: ## Log in to the registry
	@set -eu; \
	test -n "$(REGISTRY)" || { printf '%s\n' "login: set REGISTRY to the registry host." >&2; exit 1; }; \
	test -n "$${REGISTRY_USER:-}" || { printf '%s\n' "REGISTRY_USER is required" >&2; exit 1; }; \
	test -n "$${REGISTRY_TOKEN:-}" || { printf '%s\n' "REGISTRY_TOKEN is required" >&2; exit 1; }; \
	printf '%s\n' "$$REGISTRY_TOKEN" | podman login "$(REGISTRY)" --username "$$REGISTRY_USER" --password-stdin
endif

-include .claude/skills/record/index.mk

# After the fragments this file includes. A fragment must not replace it.
.DEFAULT_GOAL := help

endif
