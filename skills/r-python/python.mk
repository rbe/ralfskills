# The Python tooling target of a project: python-tooling. A project
# includes this file after project.mk or sdlc.mk, from the installed
# skill, and does not keep a copy of the target in its Makefile.
#
#     include .claude/skills/r-project-setup/project.mk
#     include .claude/skills/r-python/python.mk
#
# Python runs through $(PYTHON), which is Podman on this machine, from
# podman-python.mk of r-project-setup. This file needs no variable of
# its own.
#
# A new project, or a project with no .coveragerc yet, runs
#   make python-tooling
# once. A file already in the project stays as it is.
#
# GNU Make 3.81. See project.mk for the rules of a recipe.

ifndef PYTHON_MK
PYTHON_MK := 1

.PHONY: python-tooling

# One target for the Python tooling, every step through Podman:
# 1. .coveragerc from the r-python skill and .editorconfig from
#    r-project-setup, each one when missing
# 2. build/, __pycache__/, *.pyc, .ruff_cache/, and .venv/ in .gitignore,
#    each line when missing
# 3. make format-fix, so make format passes from the first commit
# Ruff and diff-cover are container images, so nothing is installed.
# A file already in the project stays as it is.
# help-group: Tools
python-tooling: ## Set up .coveragerc, EditorConfig, and .gitignore, then format
	@set -eu; \
	if [ ! -f .coveragerc ]; then cp .claude/skills/r-python/templates/coveragerc .coveragerc; fi; \
	if [ ! -f .editorconfig ]; then cp .claude/skills/r-project-setup/templates/editorconfig .editorconfig; fi; \
	touch .gitignore; \
	for line in build/ __pycache__/ '*.pyc' .ruff_cache/ .venv/; do \
	  if ! grep -qx "$$line" .gitignore; then printf '%s\n' "$$line" >> .gitignore; fi; \
	done; \
	$(MAKE) --no-print-directory format-fix

# help is the default goal. This fragment does not take it.
.DEFAULT_GOAL := help

endif
