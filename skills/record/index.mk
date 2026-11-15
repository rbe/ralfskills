# Indexes an agent reads. project.mk and sdlc.mk include this file when
# it is installed. Python runs through $(PYTHON), which is Podman on
# this machine. podman-python.mk defines it.
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

ifndef PYTHON
include $(RECORD_DIR)../project-setup/podman-python.mk
endif

.PHONY: toon ids ids-retire

toon: ## Write the ADR index and the skill index
	$(PYTHON) "$(RECORD_DIR)scripts/toon.py"

ids: ## Reject a repeated document id
	$(PYTHON) "$(RECORD_DIR)scripts/ids.py"

ids-retire: ## Retire an id. Set ID= on the command line
	@set -eu; \
	if [ -z "$(ID)" ]; then printf '%s\n' "ids-retire: set ID=<id>" >&2; exit 1; fi
	$(PYTHON) "$(RECORD_DIR)scripts/ids.py" retire "$(ID)"

setup: toon

# help is the default goal. This fragment does not take it.
.DEFAULT_GOAL := help

endif
