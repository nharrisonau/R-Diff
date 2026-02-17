TARGET = vsftpd
ORIGINAL_REPO = original
PREVIOUS_REPO ?= previous
PREV_DIR ?= prev-safe
COPY_PREVIOUS ?= 1
CURRENT_VERSION ?= 2.3.4
NPROCS ?= $(shell nproc 2>/dev/null || sysctl -n hw.ncpu 2>/dev/null || echo 4)

SAFE_TARGET = safe/$(TARGET)
BACKDOORED_TARGET = backdoored/$(TARGET)
PREVIOUS_TARGET = $(PREV_DIR)/$(TARGET)


all: safe backdoored prev-safe


safe: $(SAFE_TARGET)

backdoored: $(BACKDOORED_TARGET)

prev-safe: $(PREVIOUS_TARGET)


$(SAFE_TARGET): $(ORIGINAL_REPO)
	rm -rf safe/
	cp -r $(ORIGINAL_REPO)/ safe/
	cd safe/ && \
		$(MAKE) -j$(NPROCS) vsftpd


$(BACKDOORED_TARGET): $(ORIGINAL_REPO) patches/backdoored.patch
	rm -rf backdoored/
	cp -r $(ORIGINAL_REPO)/ backdoored/
	cd backdoored/ && \
		patch -p1 < ../patches/backdoored.patch && \
		$(MAKE) -j$(NPROCS) vsftpd


$(PREVIOUS_TARGET): $(PREVIOUS_REPO)
	if [ "$(COPY_PREVIOUS)" = "1" ]; then \
		rm -rf $(PREV_DIR)/; \
		cp -r $(PREVIOUS_REPO)/ $(PREV_DIR); \
	fi
	# Ensure PAM/libcap link flags for upstream previous tree so symbols resolve.
	# This inserts the same link flags used by the other variants into prev-safe/Makefile.
	# Use $$ to escape $ in Makefile recipe so the shell sees a single $.
	@sed -n '1,120p' $(PREV_DIR)/Makefile >/dev/null 2>&1 || true
	@sed -i '/`\.\/vsf_findlibs\.sh`/ s/$$/ -lpam -lpam_misc -lcap -lcrypt/' $(PREV_DIR)/Makefile || true

	# upstream vsftpd normally builds with a plain Makefile
	cd $(PREV_DIR)/ && \
		$(MAKE) -j$(NPROCS) clean || true && \
		$(MAKE) -j$(NPROCS)
	@mkdir -p build/previous/safe/bin
	@if [ -f $(PREV_DIR)/$(TARGET) ]; then \
	  cp -a $(PREV_DIR)/$(TARGET) build/previous/safe/bin/; \
	elif [ -f $(PREV_DIR)/build/$(TARGET) ]; then \
	  cp -a $(PREV_DIR)/build/$(TARGET) build/previous/safe/bin/; \
	fi

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
