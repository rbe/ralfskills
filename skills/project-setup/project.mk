# Shared makefile for the Make contract. Copy it unchanged to the
# repository root as project.mk. The project Makefile is the include
# point: set HELP_LEAD when the first line of help should differ,
# include this file before any target, then define the project targets.
#
#     include project.mk
#
# GNU Make 3.81, including the macOS system make. Recipes do not use the
# one-shell option or Make 4 functions. Each recipe is one shell, joined
# with backslashes, and does not depend on shell flags from the makefile.
# The shell is POSIX sh. There is no shell-script wrapper.
#
# This file provides help as the default goal. The project Makefile
# marks its own targets phony and defines them after the include:
# setup, build, and test, plus docs when it renders docs and login
# when it publishes an image.
#
# Set before the include:
#   HELP_LEAD        first line of `make help`

ifndef PROJECT_MK
PROJECT_MK := 1

HELP_LEAD ?= Make is the only interface. A target does the same thing locally and in CI.

.DEFAULT_GOAL := help

.PHONY: help

help: ## Show the targets
	@printf '%s\n' "$(HELP_LEAD)"
	@printf '%s\n' ""
	@awk 'BEGIN {FS = ":.*## "}; /^[a-zA-Z][a-zA-Z0-9_-]*:.*## / {printf "  %-32s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

endif
