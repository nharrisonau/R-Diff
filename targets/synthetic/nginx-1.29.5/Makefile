TARGET = objs/nginx
ORIGINAL_REPO = original
PREVIOUS_REPO ?= previous
PREVIOUS_DIR ?= previous
COPY_PREVIOUS ?= 1
CURRENT_VERSION ?= 1.29.5
CURRENT_TAG ?= release-1.29.5
PREVIOUS_TAG ?= release-1.29.4

SAFE_DIR = safe
BACKDOORED_DIR = backdoored

SAFE_TARGET = $(SAFE_DIR)/$(TARGET)
BACKDOORED_TARGET = $(BACKDOORED_DIR)/$(TARGET)
PREVIOUS_TARGET = $(PREVIOUS_DIR)/$(TARGET)

PATCH_BACKDOOR = patches/backdoored.patch

JOBS ?= $(shell nproc 2>/dev/null || sysctl -n hw.ncpu 2>/dev/null || echo 4)

.PHONY: all clean safe backdoored previous setup teardown print-target print-current-version
all: safe backdoored previous

safe: $(SAFE_TARGET)
backdoored: $(BACKDOORED_TARGET)
previous: $(PREVIOUS_TARGET)

define build_nginx
	set -e; \
	./auto/configure \
		--with-http_stub_status_module \
		--without-http_rewrite_module \
		--without-http_gzip_module; \
	$(MAKE) -j$(JOBS)
endef

$(SAFE_TARGET): $(ORIGINAL_REPO)
	rm -rf $(SAFE_DIR)/
	mkdir -p $(SAFE_DIR)/
	git -C $(ORIGINAL_REPO) archive --format=tar $(CURRENT_TAG) | tar -xf - -C $(SAFE_DIR)/
	cd $(SAFE_DIR) && $(build_nginx)
	@test -f "$@"

$(BACKDOORED_TARGET): $(ORIGINAL_REPO) $(PATCH_BACKDOOR)
	rm -rf $(BACKDOORED_DIR)/
	mkdir -p $(BACKDOORED_DIR)/
	git -C $(ORIGINAL_REPO) archive --format=tar $(CURRENT_TAG) | tar -xf - -C $(BACKDOORED_DIR)/
	cd $(BACKDOORED_DIR) && \
		patch -p1 < ../$(PATCH_BACKDOOR) && \
		$(build_nginx)
	@test -f "$@"

$(PREVIOUS_TARGET): $(PREVIOUS_REPO)
	if [ "$(COPY_PREVIOUS)" = "1" ]; then \
		rm -rf $(PREVIOUS_DIR)/; \
		mkdir -p $(PREVIOUS_DIR)/; \
		git -C $(PREVIOUS_REPO) archive --format=tar $(PREVIOUS_TAG) | tar -xf - -C $(PREVIOUS_DIR)/; \
	fi
	cd $(PREVIOUS_DIR) && $(build_nginx)
	@test -f "$@"

clean:
	rm -rf $(SAFE_DIR)/ $(BACKDOORED_DIR)/ $(PREVIOUS_DIR)/ previous-*/ previous-src/ previous-artifacts/

setup:
	# No-op.

teardown:
	# No-op.

print-target:
	@echo $(TARGET)

print-current-version:
	@echo $(CURRENT_VERSION)
