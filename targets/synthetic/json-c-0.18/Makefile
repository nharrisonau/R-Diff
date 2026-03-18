TARGET = json_parse
ORIGINAL_REPO = original
PREVIOUS_REPO ?= previous
PREVIOUS_DIR ?= previous-build
COPY_PREVIOUS ?= 1
CURRENT_VERSION ?= 0.18
CURRENT_TAG ?= json-c-0.18-20240915
PREVIOUS_TAG ?= json-c-0.17-20230812

SAFE_DIR = safe
BACKDOORED_DIR = backdoored

SAFE_TARGET = $(SAFE_DIR)/$(TARGET)
BACKDOORED_TARGET = $(BACKDOORED_DIR)/$(TARGET)
PREVIOUS_TARGET = $(PREVIOUS_DIR)/$(TARGET)

PATCH_BASE = patches/base.patch
PATCH_BACKDOOR = patches/backdoored.patch

JOBS ?= $(shell nproc 2>/dev/null || sysctl -n hw.ncpu 2>/dev/null || echo 4)
CC ?= cc
CFLAGS ?= -O2 -Wall -Wextra -std=c11
JSON_C_SOURCES = \
	arraylist.c \
	debug.c \
	json_c_version.c \
	json_object.c \
	json_object_iterator.c \
	json_tokener.c \
	json_util.c \
	json_visit.c \
	linkhash.c \
	printbuf.c \
	random_seed.c \
	strerror_override.c \
	json_pointer.c \
	json_patch.c

.PHONY: all clean safe backdoored previous setup teardown print-target print-current-version
all: safe backdoored previous

safe: $(SAFE_TARGET)
backdoored: $(BACKDOORED_TARGET)
previous: $(PREVIOUS_TARGET)

define build_json_c
	set -e; \
	printf '%s\n' \
		'/* generated for synthetic native-build sample */' \
		'#define STDC_HEADERS 1' \
		'#define HAVE_DLFCN_H 1' \
		'#define HAVE_ENDIAN_H 1' \
		'#define HAVE_FCNTL_H 1' \
		'#define HAVE_INTTYPES_H 1' \
		'#define HAVE_LIMITS_H 1' \
		'#define HAVE_LOCALE_H 1' \
		'#define HAVE_MEMORY_H 1' \
		'#define HAVE_STDARG_H 1' \
		'#define HAVE_STDINT_H 1' \
		'#define HAVE_STDLIB_H 1' \
		'#define HAVE_STRINGS_H 1' \
		'#define HAVE_STRING_H 1' \
		'#define HAVE_SYSLOG_H 1' \
		'#define HAVE_SYS_CDEFS_H 1' \
		'#define HAVE_SYS_PARAM_H 1' \
		'#define HAVE_SYS_RANDOM_H 1' \
		'#define HAVE_SYS_RESOURCE_H 1' \
		'#define HAVE_SYS_STAT_H 1' \
		'#define HAVE_SYS_TYPES_H 1' \
		'#define HAVE_UNISTD_H 1' \
		'#define HAVE_OPEN 1' \
		'#define HAVE_REALLOC 1' \
		'#define HAVE_SETLOCALE 1' \
		'#define HAVE_SNPRINTF 1' \
		'#define HAVE_STRCASECMP 1' \
		'#define HAVE_STRDUP 1' \
		'#define HAVE_STRERROR 1' \
		'#define HAVE_STRNCASECMP 1' \
		'#define HAVE_USELOCALE 1' \
		'#define HAVE_VASPRINTF 1' \
		'#define HAVE_VPRINTF 1' \
		'#define HAVE_VSNPRINTF 1' \
		'#define HAVE_VSYSLOG 1' \
		'#define HAVE_GETRANDOM 1' \
		'#define HAVE_GETRUSAGE 1' \
		'#define HAVE_STRTOLL 1' \
		'#define HAVE_STRTOULL 1' \
		'#define HAVE___THREAD 1' \
		'#define SPEC___THREAD __thread' \
		'#define HAVE_ATOMIC_BUILTINS 1' \
		'#define HAVE_DECL_INFINITY 1' \
		'#define HAVE_DECL_ISINF 1' \
		'#define HAVE_DECL_ISNAN 1' \
		'#define HAVE_DECL_NAN 1' \
		'#define HAVE_DECL__FINITE 0' \
		'#define HAVE_DECL__ISNAN 0' \
		'/* #undef HAVE_ARC4RANDOM */' \
		'#define JSON_C_HAVE_INTTYPES_H 1' \
		'#define SIZEOF_INT 4' \
		'#define SIZEOF_INT64_T 8' \
		'#define SIZEOF_LONG 8' \
		'#define SIZEOF_LONG_LONG 8' \
		'#define SIZEOF_SIZE_T 8' \
		'#define SIZEOF_SSIZE_T 8' \
		'#define PACKAGE "json-c"' \
		'#define PACKAGE_BUGREPORT "https://github.com/json-c/json-c/issues"' \
		'#define PACKAGE_NAME "json-c"' \
		'#define PACKAGE_STRING "json-c 0.18"' \
		'#define PACKAGE_TARNAME "json-c"' \
		'#define PACKAGE_URL "https://github.com/json-c/json-c"' \
		'#define PACKAGE_VERSION "0.18"' \
		'#define VERSION "0.18"' \
		> config.h; \
	printf '%s\n' \
		'/* generated for synthetic native-build sample */' \
		'#define JSON_C_HAVE_INTTYPES_H 1' \
		> json_config.h; \
	printf '%s\n' \
		'#ifndef _json_h_' \
		'#define _json_h_' \
		'' \
		'#ifdef __cplusplus' \
		'extern "C" {' \
		'#endif' \
		'' \
		'#include "arraylist.h"' \
		'#include "debug.h"' \
		'#include "json_c_version.h"' \
		'#include "json_object.h"' \
		'#include "json_object_iterator.h"' \
		'#include "json_patch.h"' \
		'#include "json_pointer.h"' \
		'#include "json_tokener.h"' \
		'#include "json_util.h"' \
		'#include "linkhash.h"' \
		'' \
		'#ifdef __cplusplus' \
		'}' \
		'#endif' \
		'' \
		'#endif' \
		> json.h; \
	printf '%s\n' \
		'/* generated for synthetic native-build sample */' \
		'#define HAVE_SYS_RESOURCE_H 1' \
		'#define HAVE_GETRUSAGE 1' \
		> apps/apps_config.h; \
	$(CC) $(CFLAGS) -D_GNU_SOURCE -I. -Iapps \
		apps/json_parse.c $(JSON_C_SOURCES) \
		-o json_parse \
		$(LDFLAGS) $(LIBS) -lm
endef

$(SAFE_TARGET): $(ORIGINAL_REPO) $(PATCH_BASE)
	rm -rf $(SAFE_DIR)/
	mkdir -p $(SAFE_DIR)/
	git -C $(ORIGINAL_REPO) archive --format=tar $(CURRENT_TAG) | tar -xf - -C $(SAFE_DIR)/
	cd $(SAFE_DIR) && \
		set -e; \
		patch -p1 < ../$(PATCH_BASE); \
		$(build_json_c)
	@test -f "$@"

$(BACKDOORED_TARGET): $(ORIGINAL_REPO) $(PATCH_BASE) $(PATCH_BACKDOOR)
	rm -rf $(BACKDOORED_DIR)/
	mkdir -p $(BACKDOORED_DIR)/
	git -C $(ORIGINAL_REPO) archive --format=tar $(CURRENT_TAG) | tar -xf - -C $(BACKDOORED_DIR)/
	cd $(BACKDOORED_DIR) && \
		set -e; \
		patch -p1 < ../$(PATCH_BASE); \
		patch -p1 < ../$(PATCH_BACKDOOR); \
		$(build_json_c)
	@test -f "$@"

$(PREVIOUS_TARGET): $(PREVIOUS_REPO) $(PATCH_BASE)
	if [ "$(COPY_PREVIOUS)" = "1" ]; then \
		rm -rf $(PREVIOUS_DIR)/; \
		mkdir -p $(PREVIOUS_DIR)/; \
		git -C $(PREVIOUS_REPO) archive --format=tar $(PREVIOUS_TAG) | tar -xf - -C $(PREVIOUS_DIR)/; \
	fi
	cd $(PREVIOUS_DIR) && \
		set -e; \
		patch -p1 < ../$(PATCH_BASE); \
		$(build_json_c)
	@test -f "$@"

clean:
	rm -rf $(SAFE_DIR)/ $(BACKDOORED_DIR)/ $(PREVIOUS_DIR)/ previous-src/ previous-artifacts/

setup:
	# No-op.

teardown:
	# No-op.

print-target:
	@echo $(TARGET)

print-current-version:
	@echo $(CURRENT_VERSION)
