TARGET = build/bin/sudo
ORIGINAL_REPO = original
PREVIOUS_REPO ?= previous
PREV_DIR ?= prev-safe
COPY_PREVIOUS ?= 1
CURRENT_VERSION ?= 1.9.15p5
# We don't want to use sudo in certain contexts (e.g., in a Docker container), so we guard it
# behind this. It will simply do nothing if sudo is not present.
SUDO := $(shell which sudo)

SAFE_TARGET = safe/$(TARGET)
BACKDOORED_TARGET = backdoored/$(TARGET)
PREVIOUS_TARGET = $(PREV_DIR)/$(TARGET)


all: safe backdoored prev-safe


safe: $(SAFE_TARGET)

backdoored: $(BACKDOORED_TARGET)

prev-safe: $(PREVIOUS_TARGET)


$(SAFE_TARGET): $(ORIGINAL_REPO)
	$(SUDO) rm -rf safe/
	cp -r $(ORIGINAL_REPO) safe/
	cd safe/ && \
		patch -p1 < ../patches/base.patch && \
		./configure --prefix=$(realpath .)/safe/build --without-pam && \
		$(SUDO) make -j32 && \
		$(SUDO) make install


$(BACKDOORED_TARGET): $(ORIGINAL_REPO) patches/backdoored.patch
	$(SUDO) rm -rf backdoored/
	cp -r $(ORIGINAL_REPO) backdoored/
	cd backdoored/ && \
		patch -p1 < ../patches/base.patch && \
		patch -p1 < ../patches/backdoored.patch && \
		./configure --prefix=$(realpath .)/backdoored/build --without-pam && \
		$(SUDO) make -j32 && \
		$(SUDO) make install


$(PREVIOUS_TARGET): $(PREVIOUS_REPO)
	if [ "$(COPY_PREVIOUS)" = "1" ]; then \
		$(SUDO) rm -rf $(PREV_DIR)/; \
		cp -r $(PREVIOUS_REPO) $(PREV_DIR); \
	fi
	cd $(PREV_DIR)/ && \
		patch -p1 < ../patches/base.patch && \
		./configure --prefix=$(realpath .)/$(PREV_DIR)/build --without-pam && \
		$(SUDO) make -j32 && \
		$(SUDO) make install


clean:
	$(SUDO) rm -rf safe/ backdoored/ $(PREV_DIR)/ prev-safe-*/ baseline-src/ baseline-artifacts/

setup:
#   No-op.

teardown:
#   No-op.

print-target:
	@echo $(TARGET)

print-current-version:
	@echo $(CURRENT_VERSION)


.PHONY: clean all safe backdoored prev-safe setup teardown print-target print-current-version
