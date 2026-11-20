# Existing tools. A project does not vendor a linter or a formatter.
# editorconfig-checker reads .editorconfig.
# diff-cover writes build/coverage/diff.md for the lines this change
# touched. The recipe sets REPORT to the Cobertura, JaCoCo, or lcov
# file. fail-under is 0: the report is the lines, not a percentage gate.
# Python runs in the image from podman-python.mk. Include that file first.

ifndef PROJECT_TOOLS_MK
PROJECT_TOOLS_MK := 1

EDITORCONFIG_IMAGE ?= ghcr.io/editorconfig-checker/editorconfig-checker:4.0.2
RUFF_IMAGE ?= ghcr.io/astral-sh/ruff:0.15.2
COVERAGE_VERSION ?= 7.17.3
DIFF_COVER_VERSION ?= 11.0.2

EDITORCONFIG = podman run --rm -v "$(CURDIR)":/check:Z $(EDITORCONFIG_IMAGE)

# diff-cover needs git. This image has git and Python, so the recipe
# installs no system package.
DIFF_COVER_IMAGE ?= docker.io/library/python:3.13

DIFF_COVER = podman run --rm -e HOME=/tmp -e PYTHONDONTWRITEBYTECODE=1 -e REPORT -v "$(CURDIR)":/work:Z -w /work $(DIFF_COVER_IMAGE) sh -c 'set -eu; git config --global --add safe.directory /work; pip install --disable-pip-version-check --root-user-action=ignore -q --target /tmp/py "diff-cover==$(DIFF_COVER_VERSION)"; PYTHONPATH=/tmp/py python3 -m diff_cover.diff_cover_tool "$$REPORT" --diff-file build/coverage/change.diff --format markdown:build/coverage/diff.md --fail-under=0'

# help is the default goal. This fragment does not take it.
.DEFAULT_GOAL := help

endif
