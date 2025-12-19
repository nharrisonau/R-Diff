SHELL := /usr/bin/env bash

# Only include dirs that actually look buildable (have Makefile/makefile/build.sh)
COMP_AUTH_DIRS := $(sort $(patsubst %/,%,$(dir \
  $(wildcard components/authentic/*/Makefile) \
)))
COMP_SYN_DIRS := $(sort $(patsubst %/,%,$(dir \
  $(wildcard components/synthetic/*/Makefile) \
)))

FW_SYN_DIRS := $(sort $(patsubst %/,%,$(dir \
  $(wildcard firmware/synthetic/*/build.sh) \
)))

COMPONENTS_DIRS := $(COMP_AUTH_DIRS) $(COMP_SYN_DIRS)
FIRMWARE_DIRS   := $(FW_SYN_DIRS)
TARGETS         := $(COMPONENTS_DIRS) $(FIRMWARE_DIRS)

all: $(TARGETS)

components: $(COMPONENTS_DIRS)
components-authentic: $(COMP_AUTH_DIRS)
components-synthetic: $(COMP_SYN_DIRS)

firmware: $(FIRMWARE_DIRS)
firmware-synthetic: $(FW_SYN_DIRS)

# One dispatcher rule for everything in TARGETS
$(TARGETS): FORCE
	@echo "==> building $@"
	@if [[ -f "$@/Makefile" || -f "$@/makefile" ]]; then \
		$(MAKE) -C "$@"; \
	elif [[ -x "$@/build.sh" ]]; then \
		(cd "$@" && ./build.sh); \
	else \
		echo "ERROR: No Makefile/makefile or executable build.sh in $@"; \
		exit 1; \
	fi

# Helpful when debugging what "make all" will attempt
list-targets:
	@printf "%s\n" $(TARGETS)

clean:
	@set -euo pipefail; \
	for d in $(TARGETS); do \
		if [[ -f "$$d/Makefile" || -f "$$d/makefile" ]]; then \
			$(MAKE) -C "$$d" clean; \
		elif [[ -x "$$d/build.sh" ]]; then \
			(cd "$$d" && ./build.sh clean) || true; \
		fi; \
	done

FORCE: ;

.PHONY: all components components-authentic components-synthetic firmware firmware-synthetic clean list-targets FORCE
