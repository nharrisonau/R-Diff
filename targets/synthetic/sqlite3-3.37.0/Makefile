TARGET = sqlite3
ORIGINAL_REPO = original
PREVIOUS_REPO = previous

SAFE_TARGET = safe/$(TARGET)
BACKDOORED_TARGET = backdoored/$(TARGET)
PREV_SAFE_TARGET = prev-safe/$(TARGET)

SHELL := /usr/bin/bash
CC = gcc

all: original safe backdoored prev-safe

safe: $(SAFE_TARGET)

backdoored: $(BACKDOORED_TARGET)

prev-safe: $(PREV_SAFE_TARGET)

$(SAFE_TARGET): $(ORIGINAL_REPO)
	rm -rf safe/
	cp -r $(ORIGINAL_REPO) safe/
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
	cp -r $(ORIGINAL_REPO) backdoored/
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

$(PREV_SAFE_TARGET): $(PREVIOUS_REPO)
	rm -rf prev-safe/
	cp -r $(PREVIOUS_REPO) prev-safe/
	cd prev-safe/ && \
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
	rm -rf safe/ backdoored/ prev-safe/

setup:
#   No-op.

teardown:
#   No-op.


.PHONY: clean all safe backdoored prev-safe setup teardown
