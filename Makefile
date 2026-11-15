# Collection checks. Python runs in Podman on this machine.
include skills/project-setup/podman-python.mk

.DEFAULT_GOAL := test

.PHONY: test

test: ## Run the collection tests in Podman
	$(PYTHON) -m unittest skills/record/scripts/test_record.py tests/test_skills.py
