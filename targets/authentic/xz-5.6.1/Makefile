TARGET = src/liblzma/.libs/liblzma.so
ORIGINAL_REPO = original
PREVIOUS_REPO ?= previous
PREV_DIR ?= prev-safe
COPY_PREVIOUS ?= 1
CURRENT_VERSION ?= 5.6.1
PATCH = patches/backdoor.patch
NPROCS ?= $(shell nproc 2>/dev/null || sysctl -n hw.ncpu 2>/dev/null || echo 4)

SAFE_TARGET = safe/$(TARGET)
BACKDOORED_TARGET = backdoored/$(TARGET)
PREVIOUS_TARGET = $(PREV_DIR)/$(TARGET)

all: safe backdoored prev-safe

safe: $(SAFE_TARGET)
backdoored: $(BACKDOORED_TARGET)
prev-safe: $(PREVIOUS_TARGET)

# Safe: build from git source
$(SAFE_TARGET): $(ORIGINAL_REPO)
	rm -rf safe/
	cp -r $(ORIGINAL_REPO)/ safe/
	cd safe/ && \
		./autogen.sh --no-po4a --no-doxygen && \
		./configure --disable-static --enable-shared && \
		$(MAKE) -j$(NPROCS)

# Backdoored: recreate CVE-2024-3094 from clean source + patch.
$(BACKDOORED_TARGET): $(ORIGINAL_REPO) $(PATCH)
	rm -rf backdoored/
	cp -r $(ORIGINAL_REPO)/ backdoored/
	rm -rf backdoored/.git backdoored/.github backdoored/.gitignore backdoored/.gitmodules backdoored/.codespellrc
	cd backdoored/ && patch -sp1 < ../$(PATCH)
	cd backdoored/ && ./autogen.sh --no-po4a --no-doxygen
	mkdir -p backdoored/debian
	touch backdoored/debian/rules
	cd backdoored/ && \
		./configure --disable-static --enable-shared && \
		$(MAKE) -j$(NPROCS)

# Previous: build clean previous version
$(PREVIOUS_TARGET): $(PREVIOUS_REPO)
	if [ "$(COPY_PREVIOUS)" = "1" ]; then \
		rm -rf $(PREV_DIR)/; \
		cp -r $(PREVIOUS_REPO)/ $(PREV_DIR); \
	fi
	cd $(PREV_DIR)/ && \
		./autogen.sh --no-po4a --no-doxygen && \
		./configure --disable-static --enable-shared && \
		$(MAKE) -j$(NPROCS)

clean:
	rm -rf safe/ backdoored/ $(PREV_DIR)/ prev-safe-*/ baseline-src/ baseline-artifacts/

setup:
#   No-op.

teardown:
#   No-op.

print-target:
	@echo $(TARGET)

print-current-version:
	@echo $(CURRENT_VERSION)

.PHONY: clean all safe backdoored prev-safe setup teardown print-target print-current-version
