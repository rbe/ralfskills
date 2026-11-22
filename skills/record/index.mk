# Indexes an agent reads. project.mk and sdlc.mk include this file when
# it is installed. Python runs through $(PYTHON), which is Podman on
# this machine. podman-python.mk defines it.
#
#   make toon
#   make ids
#   make links
#   make links-check
#   make ids-retire ID=W-5 INTO="R-28 R-60"
#   make ids-retire ID=W-6
#
# toon writes docs/adr/index.toon and docs/skill-index.toon.
# A repository with docs/REQUIREMENTS.md and no ADR file writes
# docs/requirements-index.toon instead, and does not create docs/adr/.
# When both exist, toon writes the ADR index.
# make setup runs toon first when this file is included.

ifndef RECORD_INDEX_MK
RECORD_INDEX_MK := 1

RECORD_DIR := $(dir $(lastword $(MAKEFILE_LIST)))

ifndef PYTHON
include $(RECORD_DIR)../project-setup/podman-python.mk
endif

.PHONY: toon ids ids-retire links links-check

toon: ## Write the ADR or requirements index, and the skill index
	$(PYTHON) "$(RECORD_DIR)scripts/toon.py"

ids: ## Reject a repeated id, and a list that names an id that does not resolve
	$(PYTHON) "$(RECORD_DIR)scripts/ids.py"

ids-retire: ## Retire an id. Set ID=, and INTO= for the ids that took its content
	@set -eu; \
	if [ -z "$(ID)" ]; then printf '%s\n' "ids-retire: set ID=<id>" >&2; exit 1; fi
	$(PYTHON) "$(RECORD_DIR)scripts/ids.py" retire "$(ID)" $(INTO)

links: ## Write a link for each id in the documents under docs/
	$(PYTHON) "$(RECORD_DIR)scripts/links.py"

links-check: ## Fail when an id in a document is not a link
	$(PYTHON) "$(RECORD_DIR)scripts/links.py" check

setup: toon

# GNU Make 3.81 joins the prerequisites of two setup rules in the reverse
# order of the includes. When doctor.mk is included, toon waits for doctor,
# so doctor runs first in every Make version.
ifdef DOCTOR_MK
toon: doctor
endif

# help is the default goal. This fragment does not take it.
.DEFAULT_GOAL := help

endif
