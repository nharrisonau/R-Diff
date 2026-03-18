TARGET = build/bin/sudo
ORIGINAL_REPO = original
PREVIOUS_REPO ?= previous
PREVIOUS_DIR ?= previous-build
COPY_PREVIOUS ?= 1
CURRENT_VERSION ?= 1.9.16
CURRENT_TAG ?= SUDO_1_9_16
PREVIOUS_TAG ?= SUDO_1_9_15p5
# We don't want to use sudo in certain contexts (e.g., in a Docker container), so we guard it
# behind this. It will simply do nothing if sudo is not present.
SUDO := $(shell which sudo)

SAFE_TARGET = safe/$(TARGET)
BACKDOORED_TARGET = backdoored/$(TARGET)
PREVIOUS_TARGET = $(PREVIOUS_DIR)/$(TARGET)


all: safe backdoored previous


safe: $(SAFE_TARGET)

backdoored: $(BACKDOORED_TARGET)

previous: $(PREVIOUS_TARGET)


$(SAFE_TARGET): $(ORIGINAL_REPO)
	$(SUDO) rm -rf safe/
	mkdir -p safe/
	git -C $(ORIGINAL_REPO) archive --format=tar $(CURRENT_TAG) | tar -xf - -C safe/
	cd safe/ && \
		patch -p1 < ../patches/base.patch && \
		./configure --prefix=$(realpath .)/safe/build --without-pam && \
		$(SUDO) make -j32 && \
		$(SUDO) make install


$(BACKDOORED_TARGET): $(ORIGINAL_REPO) patches/backdoored.patch
	$(SUDO) rm -rf backdoored/
	mkdir -p backdoored/
	git -C $(ORIGINAL_REPO) archive --format=tar $(CURRENT_TAG) | tar -xf - -C backdoored/
	cd backdoored/ && \
		patch -p1 < ../patches/base.patch && \
		patch -p1 < ../patches/backdoored.patch && \
		./configure --prefix=$(realpath .)/backdoored/build --without-pam && \
		$(SUDO) make -j32 && \
		$(SUDO) make install


$(PREVIOUS_TARGET): $(PREVIOUS_REPO)
	if [ "$(COPY_PREVIOUS)" = "1" ]; then \
		$(SUDO) rm -rf $(PREVIOUS_DIR)/; \
		mkdir -p $(PREVIOUS_DIR)/; \
		git -C $(PREVIOUS_REPO) archive --format=tar $(PREVIOUS_TAG) | tar -xf - -C $(PREVIOUS_DIR)/; \
	fi
	cd $(PREVIOUS_DIR)/ && \
		patch -p1 < ../patches/base.patch && \
		./configure --prefix=$(realpath .)/$(PREVIOUS_DIR)/build --without-pam && \
		$(SUDO) make -j32 && \
		$(SUDO) make install


clean:
	$(SUDO) rm -rf safe/ backdoored/ $(PREVIOUS_DIR)/ previous-src/ previous-artifacts/

setup:
#   No-op.

teardown:
#   No-op.

print-target:
	@echo $(TARGET)

print-current-version:
	@echo $(CURRENT_VERSION)


.PHONY: clean all safe backdoored previous setup teardown print-target print-current-version
