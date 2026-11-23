# Indexes an agent reads. project.mk and sdlc.mk include this file when
# it is installed. Python runs through $(PYTHON), which is Podman on
# this machine. podman-python.mk defines it.
#
#   make toon
#   make ids
#   make links
#   make links-check
#   make id KIND=W
#   make id-raise KIND=D TO=24
#
# id prints the next id of a kind (R, W, ADR, or P) and raises the
# counter of that kind in docs/ids.yaml by one. A number is never given
# twice. id-raise sets a counter to a higher number, for the ids that
# a repository already uses.
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

.PHONY: toon ids id id-raise links links-check

toon: ## Write the ADR or requirements index, and the skill index
	$(PYTHON) "$(RECORD_DIR)scripts/toon.py"

ids: ## Reject a repeated id, an id above its counter, and a list item that is no id
	$(PYTHON) "$(RECORD_DIR)scripts/ids.py"

id: ## Print the next id of a kind and raise its counter. Set KIND=R, W, ADR, or P
	@set -eu; \
	if [ -z "$(KIND)" ]; then printf '%s\n' "id: set KIND=<R, W, ADR, or P>" >&2; exit 1; fi; \
	$(PYTHON) "$(RECORD_DIR)scripts/ids.py" id "$(KIND)"

id-raise: ## Set the counter of a kind to a higher number. Set KIND= and TO=
	@set -eu; \
	if [ -z "$(KIND)" ] || [ -z "$(TO)" ]; then printf '%s\n' "id-raise: set KIND=<kind> and TO=<number>" >&2; exit 1; fi; \
	$(PYTHON) "$(RECORD_DIR)scripts/ids.py" raise "$(KIND)" "$(TO)"

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
