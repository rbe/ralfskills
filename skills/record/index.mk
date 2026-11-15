# Indexes an agent reads. project.mk and sdlc.mk include this file when
# it is installed. Make is the interface. Python reads the frontmatter.
#
#   make toon
#
# Writes docs/adr/index.toon and docs/skill-index.toon. make setup runs
# this target first when this file is included.

ifndef RECORD_INDEX_MK
RECORD_INDEX_MK := 1

RECORD_DIR := $(dir $(lastword $(MAKEFILE_LIST)))

.PHONY: toon

toon: ## Write the ADR index and the skill index
	python3 "$(RECORD_DIR)scripts/toon.py"

setup: toon

endif
