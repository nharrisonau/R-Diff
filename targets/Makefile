BASELINES_CONFIG ?= malicious/baselines_config.json
BASELINES_OUT ?= ../local_outputs/malicious/baselines.csv
STRICT ?= 0

# Use baselines_config.json as the source of truth for which malicious targets exist.
# This avoids accidentally building stray/untracked directories under malicious/*.
ifneq ($(wildcard $(BASELINES_CONFIG)),)
MALICIOUS_AUTHENTIC_TARGETS := $(shell python3 -c "import json, pathlib; cfg=json.load(open('$(BASELINES_CONFIG)')); print(' '.join(pathlib.Path(e['path']).name for e in cfg if e.get('group')=='authentic'))")
MALICIOUS_SYNTHETIC_TARGETS := $(shell python3 -c "import json, pathlib; cfg=json.load(open('$(BASELINES_CONFIG)')); print(' '.join(pathlib.Path(e['path']).name for e in cfg if e.get('group')=='synthetic'))")
else
MALICIOUS_AUTHENTIC_DIRS = $(wildcard malicious/authentic/*)
MALICIOUS_SYNTHETIC_DIRS = $(wildcard malicious/synthetic/*)
MALICIOUS_AUTHENTIC_TARGETS = $(MALICIOUS_AUTHENTIC_DIRS:malicious/authentic/%=%)
MALICIOUS_SYNTHETIC_TARGETS = $(MALICIOUS_SYNTHETIC_DIRS:malicious/synthetic/%=%)
endif

MALICIOUS_AUTHENTIC_DIRS := $(addprefix malicious/authentic/,$(MALICIOUS_AUTHENTIC_TARGETS))
MALICIOUS_SYNTHETIC_DIRS := $(addprefix malicious/synthetic/,$(MALICIOUS_SYNTHETIC_TARGETS))
MALICIOUS_TARGETS = $(MALICIOUS_AUTHENTIC_TARGETS) $(MALICIOUS_SYNTHETIC_TARGETS)

all: malicious-baselines

malicious: submodules malicious-current

malicious-authentic: submodules malicious-authentic-current

malicious-synthetic: submodules malicious-synthetic-current

malicious-current: malicious-authentic-current malicious-synthetic-current

malicious-authentic-current:
	@fail=0; \
	for dir in $(MALICIOUS_AUTHENTIC_DIRS); do \
		echo "==> Building $$dir"; \
		if ! $(MAKE) -C $$dir SUDO=; then \
			echo "WARN: build failed: $$dir"; \
			fail=1; \
			if [ "$(STRICT)" = "1" ]; then exit 2; fi; \
		fi; \
	done; \
	if [ "$$fail" -ne 0 ] && [ "$(STRICT)" = "1" ]; then exit 2; fi

malicious-synthetic-current:
	@fail=0; \
	for dir in $(MALICIOUS_SYNTHETIC_DIRS); do \
		echo "==> Building $$dir"; \
		if ! $(MAKE) -C $$dir SUDO=; then \
			echo "WARN: build failed: $$dir"; \
			fail=1; \
			if [ "$(STRICT)" = "1" ]; then exit 2; fi; \
		fi; \
	done; \
	if [ "$$fail" -ne 0 ] && [ "$(STRICT)" = "1" ]; then exit 2; fi

malicious-baselines: submodules malicious-current
	python3 malicious/scripts/build_baselines.py --config "$(BASELINES_CONFIG)" --out "$(BASELINES_OUT)"

submodules:
	@cd .. && { \
		if git submodule status --recursive | grep -qE '^-'; then \
			echo "Initializing git submodules (missing sources detected)..."; \
			git submodule sync --recursive; \
			git submodule update --init --recursive; \
		else \
			echo "Git submodules already initialized."; \
		fi; \
	}

%: malicious/authentic/%
	# Force sudo off for sub-builds to avoid interactive prompts on hosts that have sudo installed.
	$(MAKE) -C $< SUDO=

%: malicious/synthetic/%
	# Force sudo off for sub-builds to avoid interactive prompts on hosts that have sudo installed.
	$(MAKE) -C $< SUDO=


clean:
	for authentic_dir in $(MALICIOUS_AUTHENTIC_DIRS); do \
		$(MAKE) -C $$authentic_dir clean SUDO=; \
	done
	for synthetic_dir in $(MALICIOUS_SYNTHETIC_DIRS); do \
		$(MAKE) -C $$synthetic_dir clean SUDO=; \
	done


FORCE: ;

.PHONY: all clean FORCE malicious malicious-authentic malicious-synthetic malicious-current malicious-authentic-current malicious-synthetic-current malicious-baselines
