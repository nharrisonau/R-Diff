TARGET = src/liblzma/.libs/liblzma.so
ORIGINAL_REPO = original
PREVIOUS_REPO ?= previous
PREVIOUS_DIR ?= previous
COPY_PREVIOUS ?= 1
CURRENT_VERSION ?= 5.6.1
PATCH = patches/backdoor.patch
NPROCS ?= $(shell nproc 2>/dev/null || sysctl -n hw.ncpu 2>/dev/null || echo 4)

SAFE_TARGET = safe/$(TARGET)
BACKDOORED_TARGET = backdoored/$(TARGET)
PREVIOUS_TARGET = $(PREVIOUS_DIR)/$(TARGET)

all: safe backdoored previous

safe: $(SAFE_TARGET)
backdoored: $(BACKDOORED_TARGET)
previous: $(PREVIOUS_TARGET)

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
		rm -rf $(PREVIOUS_DIR)/; \
		cp -r $(PREVIOUS_REPO)/ $(PREVIOUS_DIR); \
	fi
	cd $(PREVIOUS_DIR)/ && \
		./autogen.sh --no-po4a --no-doxygen && \
		./configure --disable-static --enable-shared && \
		$(MAKE) -j$(NPROCS)

clean:
	rm -rf safe/ backdoored/ $(PREVIOUS_DIR)/ previous-*/ previous-src/ previous-artifacts/

setup:
#   No-op.

teardown:
#   No-op.

print-target:
	@echo $(TARGET)

print-current-version:
	@echo $(CURRENT_VERSION)

.PHONY: clean all safe backdoored previous setup teardown print-target print-current-version
