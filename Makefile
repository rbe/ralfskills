# Collection checks. Python runs in Podman on this machine.
# `make` prints help. `make test` runs the checks.
# Ruff is the formatter and the linter. editorconfig-checker reads
# .editorconfig. diff-cover writes the lines this change touched.

# No install step. Ruff and editorconfig-checker are container images.
SETUP_CMD = true
BUILD_CMD = true
TEST_CMD = $(PYTHON) -m unittest skills/record/scripts/test_record.py tests/test_skills.py
FORMAT_CMD = podman run --rm -v "$(CURDIR)":/io:Z -w /io $(RUFF_IMAGE) format --check
LINT_CMD = podman run --rm -v "$(CURDIR)":/io:Z -w /io $(RUFF_IMAGE) check
INTEGRATION_CMD = $(PYTHON) -m unittest tests/test_integration.py
COVERAGE_CMD = set -eu; \
	base=$$(git merge-base HEAD origin/main 2>/dev/null || printf '%s' HEAD); \
	git diff "$$base" > build/coverage/change.diff; \
	podman run --rm -e HOME=/tmp -e PYTHONDONTWRITEBYTECODE=1 -v "$(CURDIR)":/work:Z -w /work $(PYTHON_IMAGE) sh -c 'set -eu; pip install --disable-pip-version-check --root-user-action=ignore -q --target /tmp/py "coverage==$(COVERAGE_VERSION)"; PYTHONPATH=/tmp/py python3 -m coverage run --rcfile=.coveragerc -m unittest skills/record/scripts/test_record.py tests/test_skills.py; PYTHONPATH=/tmp/py python3 -m coverage xml --rcfile=.coveragerc -o build/coverage/coverage.xml'; \
	REPORT=build/coverage/coverage.xml $(DIFF_COVER)

include skills/project-setup/project.mk

.DEFAULT_GOAL := help
