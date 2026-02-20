TARGET = json_parse
ORIGINAL_REPO = original
PREVIOUS_REPO ?= previous
PREV_DIR ?= prev-safe
COPY_PREVIOUS ?= 1
CURRENT_VERSION ?= 0.18
CURRENT_TAG ?= json-c-0.18-20240915
PREVIOUS_TAG ?= json-c-0.17-20230812

SAFE_TARGET = safe/$(TARGET)
BACKDOORED_TARGET = backdoored/$(TARGET)
PREVIOUS_TARGET = $(PREV_DIR)/$(TARGET)

CC ?= cc
CFLAGS += -O2 -Wall -Wextra -std=c11

all: safe backdoored prev-safe

safe: $(SAFE_TARGET)
backdoored: $(BACKDOORED_TARGET)
prev-safe: $(PREVIOUS_TARGET)

$(SAFE_TARGET): $(ORIGINAL_REPO) patches/base.patch
	rm -rf safe/
	mkdir -p safe/
	git -C $(ORIGINAL_REPO) archive --format=tar $(CURRENT_TAG) | tar -xf - -C safe/
	cd safe/ && \
		patch -p1 < ../patches/base.patch && \
		mkdir -p "$(dir $(TARGET))" && \
		$(CC) $(CFLAGS) rdiff_harness.c -o "$(TARGET)"

$(BACKDOORED_TARGET): $(ORIGINAL_REPO) patches/base.patch patches/backdoored.patch
	rm -rf backdoored/
	mkdir -p backdoored/
	git -C $(ORIGINAL_REPO) archive --format=tar $(CURRENT_TAG) | tar -xf - -C backdoored/
	cd backdoored/ && \
		patch -p1 < ../patches/base.patch && \
		patch -p1 < ../patches/backdoored.patch && \
		mkdir -p "$(dir $(TARGET))" && \
		$(CC) $(CFLAGS) rdiff_harness.c -o "$(TARGET)"

$(PREVIOUS_TARGET): $(PREVIOUS_REPO) patches/base.patch
	if [ "$(COPY_PREVIOUS)" = "1" ]; then \
		rm -rf $(PREV_DIR)/; \
		mkdir -p $(PREV_DIR)/; \
		git -C $(PREVIOUS_REPO) archive --format=tar $(PREVIOUS_TAG) | tar -xf - -C $(PREV_DIR)/; \
	fi
	cd $(PREV_DIR)/ && \
		patch -p1 < ../patches/base.patch && \
		mkdir -p "$(dir $(TARGET))" && \
		$(CC) $(CFLAGS) rdiff_harness.c -o "$(TARGET)"

clean:
	rm -rf safe/ backdoored/ $(PREV_DIR)/ prev-safe-*/ baseline-src/ baseline-artifacts/

setup:
	# No-op.

teardown:
	# No-op.

print-target:
	@echo $(TARGET)

print-current-version:
	@echo $(CURRENT_VERSION)

.PHONY: clean all safe backdoored prev-safe setup teardown print-target print-current-version
