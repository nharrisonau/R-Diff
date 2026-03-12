TARGET = sapi/cli/php
ORIGINAL_REPO = original
PREVIOUS_REPO ?= previous
PREVIOUS_DIR ?= previous
COPY_PREVIOUS ?= 1
CURRENT_VERSION ?= 8.1.0-dev

SAFE_TARGET = safe/$(TARGET)
BACKDOORED_TARGET = backdoored/$(TARGET)
PREVIOUS_TARGET = $(PREVIOUS_DIR)/$(TARGET)


all: safe backdoored previous


safe: $(SAFE_TARGET)

backdoored: $(BACKDOORED_TARGET)

previous: $(PREVIOUS_TARGET)


$(SAFE_TARGET): $(ORIGINAL_REPO) patches/safe.patch
	rm -rf safe/
	cp -r $(ORIGINAL_REPO)/ safe/
	cd safe/ && \
		patch -p1 < ../patches/safe.patch && \
		./buildconf --force && \
		./configure --with-zlib && \
		$(MAKE) -j$$(nproc) $(TARGET)


$(BACKDOORED_TARGET): $(ORIGINAL_REPO)
	rm -rf backdoored/
	cp -r $(ORIGINAL_REPO)/ backdoored/
	cd backdoored/ && \
		./buildconf && \
		./configure --with-zlib && \
		$(MAKE) -j$$(nproc) $(TARGET)


$(PREVIOUS_TARGET): $(PREVIOUS_REPO)
	if [ "$(COPY_PREVIOUS)" = "1" ]; then \
		rm -rf $(PREVIOUS_DIR)/; \
		cp -r $(PREVIOUS_REPO)/ $(PREVIOUS_DIR); \
	fi
	cd $(PREVIOUS_DIR) && \
		./buildconf --force && \
		./configure --with-zlib && \
		$(MAKE) -j$$(nproc) $(TARGET)


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
