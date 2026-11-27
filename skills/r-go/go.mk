# The Go targets of a project: go and go-tooling. A project includes this
# file after project.mk or sdlc.mk, from the installed skill, and does
# not keep a copy of the targets in its Makefile.
#
#     include .claude/skills/r-project-setup/project.mk
#     include .claude/skills/r-go/go.mk
#
# Go runs through $(GO), which is Podman on this machine. The Go caches
# are container volumes, not directories of the project. A project that
# sets GO_IMAGE, GO_CACHE, GO_OPTS, GO_RUN, GO, or MODULE before the
# include keeps its value.
#
# A new project, or a project with no go.mod yet, runs
#   make go-tooling
# once. MODULE sets the module path, for example:
#   make go-tooling MODULE=github.com/acme/app
#
# GNU Make 3.81. See project.mk for the rules of a recipe.

ifndef GO_MK
GO_MK := 1

# The module path of a new project. NAME comes from tools.mk: the
# repository name of the remote origin, else the directory name.
MODULE ?= example.com/$(NAME)
GO_IMAGE ?= docker.io/library/golang:1.25-bookworm
# The Go caches are volumes of this project. Two projects on one machine
# do not share a volume, so their containers do not wait for each other.
GO_CACHE ?= $(notdir $(CURDIR))
GO_OPTS ?= -e HOME=/tmp -e CI -e GOFLAGS=-buildvcs=false \
	-v $(GO_CACHE)-gocache:/tmp/.cache/go-build -v $(GO_CACHE)-gomod:/go/pkg/mod \
	-v "$(CURDIR)":/work:Z -w /work
GO_RUN ?= podman run --rm $(GO_OPTS) $(GO_IMAGE)
GO ?= $(GO_RUN) go
# Host mode (TOOLS=host of podman-python.mk): go runs from PATH. It
# replaces the GO_RUN and GO that the project set before the include.
ifeq ($(TOOLS),host)
GO_RUN = env GOFLAGS=-buildvcs=false
GO = $(GO_RUN) go
endif

.PHONY: go
.PHONY: go-tooling

# help-group: Tools
go: ## Run go in Podman on this machine. Set ARGS.
	@set -eu; \
	if [ -z "$(ARGS)" ]; then printf '%s\n' "go: set ARGS to the go arguments." >&2; exit 1; fi
	$(GO) $(ARGS)

# One target for the Go tooling, every step through Podman:
# 1. go.mod (go mod init MODULE) when missing
# 2. .editorconfig from r-project-setup when missing
# 3. build/ and bin/ in .gitignore, each line when missing
# 4. make format-fix, when the project has a Go package already
# gofmt and go vet come with the Go image, so nothing is installed.
# A file already in the project stays as it is.
go-tooling: ## Set up go.mod, EditorConfig, and .gitignore, then format
	@set -eu; \
	if [ ! -f go.mod ]; then $(GO) mod init $(MODULE); fi; \
	if [ ! -f .editorconfig ]; then cp .claude/skills/r-project-setup/templates/editorconfig .editorconfig; fi; \
	touch .gitignore; \
	for line in build/ bin/; do \
	  if ! grep -qx "$$line" .gitignore; then printf '%s\n' "$$line" >> .gitignore; fi; \
	done; \
	if [ -n "$$($(GO) list ./... 2>/dev/null)" ]; then $(MAKE) --no-print-directory format-fix; \
	else echo "go-tooling: no Go package yet, so nothing to format."; fi

# help is the default goal. This fragment does not take it.
.DEFAULT_GOAL := help

endif
