TARGET = vsftpd
ORIGINAL_REPO = original
PREVIOUS_REPO ?= previous
PREVIOUS_DIR ?= previous-build
COPY_PREVIOUS ?= 1
CURRENT_VERSION ?= 2.3.4
NPROCS ?= $(shell nproc 2>/dev/null || sysctl -n hw.ncpu 2>/dev/null || echo 4)

SAFE_TARGET = safe/$(TARGET)
BACKDOORED_TARGET = backdoored/$(TARGET)
PREVIOUS_TARGET = $(PREVIOUS_DIR)/$(TARGET)


all: safe backdoored previous


safe: $(SAFE_TARGET)

backdoored: $(BACKDOORED_TARGET)

previous: $(PREVIOUS_TARGET)


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
		rm -rf $(PREVIOUS_DIR)/; \
		cp -r $(PREVIOUS_REPO)/ $(PREVIOUS_DIR); \
	fi
	# Ensure PAM/libcap link flags for upstream previous tree so symbols resolve.
	# This inserts the same link flags used by the other variants into previous/Makefile.
	# Use $$ to escape $ in Makefile recipe so the shell sees a single $.
	@sed -n '1,120p' $(PREVIOUS_DIR)/Makefile >/dev/null 2>&1 || true
	@sed -i '/`\.\/vsf_findlibs\.sh`/ s/$$/ -lpam -lpam_misc -lcap -lcrypt/' $(PREVIOUS_DIR)/Makefile || true

	# upstream vsftpd normally builds with a plain Makefile
	cd $(PREVIOUS_DIR)/ && \
		$(MAKE) -j$(NPROCS) clean || true && \
		$(MAKE) -j$(NPROCS)
	@mkdir -p build/previous/safe/bin
	@if [ -f $(PREVIOUS_DIR)/$(TARGET) ]; then \
	  cp -a $(PREVIOUS_DIR)/$(TARGET) build/previous/safe/bin/; \
	elif [ -f $(PREVIOUS_DIR)/build/$(TARGET) ]; then \
	  cp -a $(PREVIOUS_DIR)/build/$(TARGET) build/previous/safe/bin/; \
	fi

clean:
	rm -rf safe/ backdoored/ $(PREVIOUS_DIR)/ previous-src/ previous-artifacts/

setup:
#   No-op.

teardown:
#   No-op.

print-target:
	@echo $(TARGET)

print-current-version:
	@echo $(CURRENT_VERSION)


.PHONY: clean all safe backdoored previous setup teardown print-target print-current-version
