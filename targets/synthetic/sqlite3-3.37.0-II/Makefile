TARGET = sqlite3
ORIGINAL_REPO = original
PREVIOUS_REPO ?= previous
PREVIOUS_DIR ?= previous-build
COPY_PREVIOUS ?= 1
CURRENT_VERSION ?= 3.37.0
CURRENT_TAG ?= version-3.37.0
PREVIOUS_TAG ?= version-3.36.0

SAFE_TARGET = safe/$(TARGET)
BACKDOORED_TARGET = backdoored/$(TARGET)
PREVIOUS_TARGET = $(PREVIOUS_DIR)/$(TARGET)

SHELL := /usr/bin/bash
CC = gcc

all: safe backdoored previous

safe: $(SAFE_TARGET)
backdoored: $(BACKDOORED_TARGET)
previous: $(PREVIOUS_TARGET)

$(SAFE_TARGET): $(ORIGINAL_REPO)
	rm -rf safe/
	mkdir -p safe/
	git -C $(ORIGINAL_REPO) archive --format=tar $(CURRENT_TAG) | tar -xf - -C safe/
	cd safe/ && \
		patch -p1 < ../patches/base.patch && \
		export CFLAGS="$(CFLAGS) -DSQLITE_MAX_LENGTH=128000000 \
               -DSQLITE_MAX_SQL_LENGTH=128000000 \
               -DSQLITE_MAX_MEMORY=25000000 \
               -DSQLITE_PRINTF_PRECISION_LIMIT=1048576 \
               -DSQLITE_DEBUG=1 \
               -DSQLITE_MAX_PAGE_COUNT=16384" && \
		./configure --disable-shared --enable-rtree && \
		$(MAKE) clean && \
		$(MAKE) -j$(shell nproc) && \
		$(MAKE) sqlite3.c && \
		$(CC) $(CFLAGS) -I. \
			"./test/ossfuzz.c" "./sqlite3.o" \
			-o "sqlite3_fuzz" \
			$(LDFLAGS) $(LIBS) -pthread -ldl -lm

$(BACKDOORED_TARGET): $(ORIGINAL_REPO) patches/backdoored.patch
	rm -rf backdoored/
	mkdir -p backdoored/
	git -C $(ORIGINAL_REPO) archive --format=tar $(CURRENT_TAG) | tar -xf - -C backdoored/
	cd backdoored/ && \
		patch -p1 < ../patches/base.patch && \
		patch -p1 < ../patches/backdoored.patch && \
		export CFLAGS="$(CFLAGS) -DSQLITE_MAX_LENGTH=128000000 \
               -DSQLITE_MAX_SQL_LENGTH=128000000 \
               -DSQLITE_MAX_MEMORY=25000000 \
               -DSQLITE_PRINTF_PRECISION_LIMIT=1048576 \
               -DSQLITE_DEBUG=1 \
               -DSQLITE_MAX_PAGE_COUNT=16384" && \
		./configure --disable-shared --enable-rtree && \
		$(MAKE) clean && \
		$(MAKE) -j$(shell nproc) && \
		$(MAKE) sqlite3.c && \
		$(CC) $(CFLAGS) -I. \
			"./test/ossfuzz.c" "./sqlite3.o" \
			-o "sqlite3_fuzz" \
			$(LDFLAGS) $(LIBS) -pthread -ldl -lm

$(PREVIOUS_TARGET): $(PREVIOUS_REPO)
	if [ "$(COPY_PREVIOUS)" = "1" ]; then \
		rm -rf $(PREVIOUS_DIR)/; \
		mkdir -p $(PREVIOUS_DIR)/; \
		git -C $(PREVIOUS_REPO) archive --format=tar $(PREVIOUS_TAG) | tar -xf - -C $(PREVIOUS_DIR)/; \
	fi
	cd $(PREVIOUS_DIR) && \
		patch -p1 < ../patches/base.patch && \
		export CFLAGS="$(CFLAGS) -DSQLITE_MAX_LENGTH=128000000 \
               -DSQLITE_MAX_SQL_LENGTH=128000000 \
               -DSQLITE_MAX_MEMORY=25000000 \
               -DSQLITE_PRINTF_PRECISION_LIMIT=1048576 \
               -DSQLITE_DEBUG=1 \
               -DSQLITE_MAX_PAGE_COUNT=16384" && \
		./configure --disable-shared --enable-rtree && \
		$(MAKE) clean && \
		$(MAKE) -j$(shell nproc) && \
		$(MAKE) sqlite3.c && \
		$(CC) $(CFLAGS) -I. \
			"./test/ossfuzz.c" "./sqlite3.o" \
			-o "sqlite3_fuzz" \
			$(LDFLAGS) $(LIBS) -pthread -ldl -lm

clean:
	rm -rf safe/ backdoored/ $(PREVIOUS_DIR)/ previous-src/ previous-artifacts/

setup:
	# No-op.

teardown:
	# No-op.

print-target:
	@echo $(TARGET)

print-current-version:
	@echo $(CURRENT_VERSION)

.PHONY: clean all safe backdoored previous setup teardown print-target print-current-version
