# Shared makefile for the Make contract. Copy it unchanged to the
# repository root as project.mk. The project Makefile sets the
# variables below and includes this file before any target. It does
# not define setup, build, or test again.
#
#     SETUP_CMD = npm ci
#     BUILD_CMD = npm run build
#     TEST_CMD = npm test
#     include project.mk
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
# help is the default goal. It lists every target in this file that has
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
#   TEST_CMD         how this project runs the tests
#   RENDER_DOCS      1 when this repository renders docs
#   DOCS_CMD         the renderer, required when RENDER_DOCS is 1
#   PUBLISH_IMAGE    1 when an image is published
#   REGISTRY         login host. Default ghcr.io

ifndef PROJECT_MK
PROJECT_MK := 1

HELP_LEAD ?= Make is the only interface. A target does the same thing locally and in CI.
REGISTRY ?= ghcr.io

.DEFAULT_GOAL := help

.PHONY: help setup build test

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
test: ## Run the tests
	@set -eu; \
	if [ -z "$(TEST_CMD)" ]; then \
	  printf '%s\n' "test: stub. Set TEST_CMD before the include. Run this project's tests." >&2; \
	  exit 1; \
	fi; \
	$(TEST_CMD)

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

endif
