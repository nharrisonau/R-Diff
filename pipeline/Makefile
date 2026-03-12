CONFIG ?= previous_config.json
PREVIOUS_OUT ?= ../local_outputs/previous.csv
TARGETS_ROOT ?= ../targets
STRICT ?= 0

# Use previous_config.json as the source of truth for which targets exist.
# This avoids accidentally building stray/untracked directories under {authentic,synthetic}.
ifneq ($(wildcard $(CONFIG)),)
AUTHENTIC_TARGETS := $(shell python3 -c "import json, pathlib; cfg=json.load(open('$(CONFIG)')); print(' '.join(pathlib.Path(e['path']).name for e in cfg if e.get('group')=='authentic'))")
SYNTHETIC_TARGETS := $(shell python3 -c "import json, pathlib; cfg=json.load(open('$(CONFIG)')); print(' '.join(pathlib.Path(e['path']).name for e in cfg if e.get('group')=='synthetic'))")
else
AUTHENTIC_DIRS = $(wildcard $(TARGETS_ROOT)/authentic/*)
SYNTHETIC_DIRS = $(wildcard $(TARGETS_ROOT)/synthetic/*)
AUTHENTIC_TARGETS = $(AUTHENTIC_DIRS:$(TARGETS_ROOT)/authentic/%=%)
SYNTHETIC_TARGETS = $(SYNTHETIC_DIRS:$(TARGETS_ROOT)/synthetic/%=%)
endif

AUTHENTIC_DIRS := $(addprefix $(TARGETS_ROOT)/authentic/,$(AUTHENTIC_TARGETS))
SYNTHETIC_DIRS := $(addprefix $(TARGETS_ROOT)/synthetic/,$(SYNTHETIC_TARGETS))
TARGETS = $(AUTHENTIC_TARGETS) $(SYNTHETIC_TARGETS)

all: previous

# Build only current variants (safe/backdoored/previous) for all targets.
current: submodules current-variants

authentic: submodules authentic-variants

synthetic: submodules synthetic-variants

current-variants: authentic-variants synthetic-variants

authentic-variants:
	@fail=0; 	for dir in $(AUTHENTIC_DIRS); do 		echo "==> Building $$dir"; 		if ! $(MAKE) -C $$dir SUDO=; then 			echo "WARN: build failed: $$dir"; 			fail=1; 			if [ "$(STRICT)" = "1" ]; then exit 2; fi; 		fi; 	done; 	if [ "$$fail" -ne 0 ] && [ "$(STRICT)" = "1" ]; then exit 2; fi

synthetic-variants:
	@fail=0; 	for dir in $(SYNTHETIC_DIRS); do 		echo "==> Building $$dir"; 		if ! $(MAKE) -C $$dir SUDO=; then 			echo "WARN: build failed: $$dir"; 			fail=1; 			if [ "$(STRICT)" = "1" ]; then exit 2; fi; 		fi; 	done; 	if [ "$$fail" -ne 0 ] && [ "$(STRICT)" = "1" ]; then exit 2; fi

# Build single selected previous artifacts (best-effort) and write previous CSV.
previous: submodules current-variants
	python3 scripts/build_previous.py --config "$(CONFIG)" --out "$(PREVIOUS_OUT)"

docs-check:
	python3 scripts/verify_target_metadata.py

submodules:
	@cd .. && { 		if git submodule status --recursive | grep -qE '^-'; then 			echo "Initializing git submodules (missing sources detected)..."; 			git submodule sync --recursive; 			git submodule update --init --recursive; 		else 			echo "Git submodules already initialized."; 		fi; 	}

%: $(TARGETS_ROOT)/authentic/%
	# Force sudo off for sub-builds to avoid interactive prompts on hosts that have sudo installed.
	$(MAKE) -C $< SUDO=

%: $(TARGETS_ROOT)/synthetic/%
	# Force sudo off for sub-builds to avoid interactive prompts on hosts that have sudo installed.
	$(MAKE) -C $< SUDO=

clean:
	for authentic_dir in $(AUTHENTIC_DIRS); do 		$(MAKE) -C $$authentic_dir clean SUDO=; 	done
	for synthetic_dir in $(SYNTHETIC_DIRS); do 		$(MAKE) -C $$synthetic_dir clean SUDO=; 	done

FORCE: ;

.PHONY: all clean FORCE submodules previous docs-check current authentic synthetic current-variants authentic-variants synthetic-variants
