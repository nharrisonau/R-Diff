TARGET = src/lighttpd
ORIGINAL_REPO = original
PREVIOUS_REPO ?= previous
PREVIOUS_DIR ?= previous-build
COPY_PREVIOUS ?= 1
CURRENT_VERSION ?= 1.4.82
CURRENT_TAG ?= lighttpd-1.4.82
PREVIOUS_TAG ?= lighttpd-1.4.81

SAFE_DIR = safe
BACKDOORED_DIR = backdoored

SAFE_TARGET = $(SAFE_DIR)/$(TARGET)
BACKDOORED_TARGET = $(BACKDOORED_DIR)/$(TARGET)
PREVIOUS_TARGET = $(PREVIOUS_DIR)/$(TARGET)

PATCH_BASE = patches/base.patch
PATCH_BACKDOOR = patches/backdoored.patch

JOBS ?= $(shell nproc 2>/dev/null || sysctl -n hw.ncpu 2>/dev/null || echo 4)

.PHONY: all clean safe backdoored previous setup teardown print-target print-current-version
all: safe backdoored previous

safe: $(SAFE_TARGET)
backdoored: $(BACKDOORED_TARGET)
previous: $(PREVIOUS_TARGET)

define build_lighttpd
	./autogen.sh; \
	./configure \
		--without-pcre2 \
		--without-pcre \
		--without-zlib \
		--without-zstd \
		--without-bzip2 \
		--without-brotli \
		--without-openssl \
		--without-gnutls \
		--without-mbedtls \
		--without-nss \
		--without-wolfssl \
		--without-nettle \
		--without-lua \
		--without-libdeflate; \
	$(MAKE) -j$(JOBS)
endef

$(SAFE_TARGET): $(ORIGINAL_REPO) $(PATCH_BASE)
	rm -rf $(SAFE_DIR)/
	mkdir -p $(SAFE_DIR)/
	git -C $(ORIGINAL_REPO) archive --format=tar $(CURRENT_TAG) | tar -xf - -C $(SAFE_DIR)/
	cd $(SAFE_DIR) && \
		patch -p1 < ../$(PATCH_BASE) && \
		$(build_lighttpd)
	@test -f "$@"

$(BACKDOORED_TARGET): $(ORIGINAL_REPO) $(PATCH_BASE) $(PATCH_BACKDOOR)
	rm -rf $(BACKDOORED_DIR)/
	mkdir -p $(BACKDOORED_DIR)/
	git -C $(ORIGINAL_REPO) archive --format=tar $(CURRENT_TAG) | tar -xf - -C $(BACKDOORED_DIR)/
	cd $(BACKDOORED_DIR) && \
		patch -p1 < ../$(PATCH_BASE) && \
		patch -p1 < ../$(PATCH_BACKDOOR) && \
		$(build_lighttpd)
	@test -f "$@"

$(PREVIOUS_TARGET): $(PREVIOUS_REPO) $(PATCH_BASE)
	if [ "$(COPY_PREVIOUS)" = "1" ]; then \
		rm -rf $(PREVIOUS_DIR)/; \
		mkdir -p $(PREVIOUS_DIR)/; \
		git -C $(PREVIOUS_REPO) archive --format=tar $(PREVIOUS_TAG) | tar -xf - -C $(PREVIOUS_DIR)/; \
	fi
	cd $(PREVIOUS_DIR) && \
		patch -p1 < ../$(PATCH_BASE) && \
		$(build_lighttpd)
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
