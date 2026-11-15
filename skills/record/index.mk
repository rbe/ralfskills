# Indexes an agent reads. project.mk and sdlc.mk include this file when
# it is installed. Make is the interface. Python runs in Podman, so the
# host does not need a Python install. Set PYTHON_IMAGE before the
# include to pick another version.
#
#   make toon
#   make ids
#   make ids-retire ID=H-2026-11-15-old
#
# toon writes docs/adr/index.toon and docs/skill-index.toon.
# make setup runs toon first when this file is included.

ifndef RECORD_INDEX_MK
RECORD_INDEX_MK := 1

RECORD_DIR := $(dir $(lastword $(MAKEFILE_LIST)))
PYTHON_IMAGE ?= docker.io/library/python:3.13-slim
RECORD_UID := $(shell id -u)
RECORD_GID := $(shell id -g)

RECORD_PY = podman run --rm --user $(RECORD_UID):$(RECORD_GID) \
	-e PYTHONDONTWRITEBYTECODE=1 \
	-v "$(CURDIR)":/work:Z -w /work \
	$(PYTHON_IMAGE) python3

.PHONY: toon ids ids-retire

toon: ## Write the ADR index and the skill index
	$(RECORD_PY) "$(RECORD_DIR)scripts/toon.py"

ids: ## Reject a repeated document id
	$(RECORD_PY) "$(RECORD_DIR)scripts/ids.py"

ids-retire: ## Retire an id. Set ID= on the command line
	@set -eu; \
	if [ -z "$(ID)" ]; then printf '%s\n' "ids-retire: set ID=<id>" >&2; exit 1; fi
	$(RECORD_PY) "$(RECORD_DIR)scripts/ids.py" retire "$(ID)"

setup: toon

endif
