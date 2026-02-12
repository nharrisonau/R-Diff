TARGET         = dropbear
ORIGINAL_REPO  = original
PREVIOUS_REPO ?= previous

SAFE_DIR       = safe
BACKDOORED_DIR = backdoored
PREV_DIR       ?= prev-safe
COPY_PREVIOUS ?= 1
CURRENT_VERSION ?= 2024.86

SAFE_TARGET        = $(SAFE_DIR)/$(TARGET)
BACKDOORED_TARGET  = $(BACKDOORED_DIR)/$(TARGET)
PREVIOUS_TARGET    = $(PREV_DIR)/$(TARGET)

PATCH_BACKDOOR = patches/backdoor.patch

JOBS ?= $(shell nproc 2>/dev/null || sysctl -n hw.ncpu 2>/dev/null || echo 4)
MAKE_FLAGS ?= -j$(JOBS)
CONFIGURE_FLAGS ?=

.PHONY: all clean safe backdoored prev-safe setup teardown print-target print-current-version
all: safe backdoored prev-safe

safe: $(SAFE_TARGET)
backdoored: $(BACKDOORED_TARGET)
prev-safe: $(PREVIOUS_TARGET)

define build_dropbear
	set -e; \
	if [ -x ./configure ]; then \
		./configure $(CONFIGURE_FLAGS); \
		$(MAKE) $(MAKE_FLAGS); \
	elif [ -f Makefile.in ] || [ -f configure.ac ] || [ -f configure.in ]; then \
		autoreconf -fi; \
		./configure $(CONFIGURE_FLAGS); \
		$(MAKE) $(MAKE_FLAGS); \
	elif [ -f Makefile ]; then \
		$(MAKE) $(MAKE_FLAGS); \
	else \
		echo "No configure/autotools/Makefile found; cannot build." >&2; \
		exit 1; \
	fi
endef

$(SAFE_TARGET): $(ORIGINAL_REPO)
	rm -rf $(SAFE_DIR)/
	cp -r $(ORIGINAL_REPO) $(SAFE_DIR)
	cd $(SAFE_DIR) && $(build_dropbear)
	@touch $@

$(BACKDOORED_TARGET): $(ORIGINAL_REPO) $(PATCH_BACKDOOR)
	rm -rf $(BACKDOORED_DIR)/
	cp -r $(ORIGINAL_REPO) $(BACKDOORED_DIR)
	cd $(BACKDOORED_DIR) && \
		patch -p1 < ../$(PATCH_BACKDOOR) && \
		$(build_dropbear)
	@touch $@

$(PREVIOUS_TARGET): $(PREVIOUS_REPO)
	if [ "$(COPY_PREVIOUS)" = "1" ]; then \
		rm -rf $(PREV_DIR)/; \
		cp -r $(PREVIOUS_REPO) $(PREV_DIR); \
	fi
	cd $(PREV_DIR) && $(build_dropbear)
	@touch $@

clean:
	rm -rf $(SAFE_DIR)/ $(BACKDOORED_DIR)/ $(PREV_DIR)/ prev-safe-*/ baseline-src/ baseline-artifacts/

setup:
	# No-op.

teardown:
	# No-op.

print-target:
	@echo $(TARGET)

print-current-version:
	@echo $(CURRENT_VERSION)
