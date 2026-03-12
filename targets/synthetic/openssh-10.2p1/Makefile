TARGET = sshd
ORIGINAL_REPO = original
PREVIOUS_REPO ?= previous
PREVIOUS_DIR ?= previous
COPY_PREVIOUS ?= 1
CURRENT_VERSION ?= 10.2p1
CURRENT_TAG ?= V_10_2_P1
PREVIOUS_TAG ?= V_10_1_P1

SAFE_DIR = safe
BACKDOORED_DIR = backdoored

SAFE_TARGET = $(SAFE_DIR)/$(TARGET)
BACKDOORED_TARGET = $(BACKDOORED_DIR)/$(TARGET)
PREVIOUS_TARGET = $(PREVIOUS_DIR)/$(TARGET)

PATCH_BACKDOOR = patches/backdoored.patch

JOBS ?= $(shell nproc 2>/dev/null || sysctl -n hw.ncpu 2>/dev/null || echo 4)
CONFIGURE_FLAGS ?= --without-openssl-header-check --without-zlib-version-check --without-pam --without-kerberos5 --without-libedit --disable-security-key

.PHONY: all clean safe backdoored previous setup teardown print-target print-current-version
all: safe backdoored previous

safe: $(SAFE_TARGET)
backdoored: $(BACKDOORED_TARGET)
previous: $(PREVIOUS_TARGET)

define build_openssh
	set -e; \
	./configure $(CONFIGURE_FLAGS); \
	$(MAKE) -j$(JOBS)
endef

$(SAFE_TARGET): $(ORIGINAL_REPO)
	rm -rf $(SAFE_DIR)/
	mkdir -p $(SAFE_DIR)/
	git -C $(ORIGINAL_REPO) archive --format=tar $(CURRENT_TAG) | tar -xf - -C $(SAFE_DIR)/
	cd $(SAFE_DIR) && $(build_openssh)
	@test -f "$@"

$(BACKDOORED_TARGET): $(ORIGINAL_REPO) $(PATCH_BACKDOOR)
	rm -rf $(BACKDOORED_DIR)/
	mkdir -p $(BACKDOORED_DIR)/
	git -C $(ORIGINAL_REPO) archive --format=tar $(CURRENT_TAG) | tar -xf - -C $(BACKDOORED_DIR)/
	cd $(BACKDOORED_DIR) && \
		patch -p2 < ../$(PATCH_BACKDOOR) && \
		$(build_openssh)
	@test -f "$@"

$(PREVIOUS_TARGET): $(PREVIOUS_REPO)
	if [ "$(COPY_PREVIOUS)" = "1" ]; then \
		rm -rf $(PREVIOUS_DIR)/; \
		mkdir -p $(PREVIOUS_DIR)/; \
		git -C $(PREVIOUS_REPO) archive --format=tar $(PREVIOUS_TAG) | tar -xf - -C $(PREVIOUS_DIR)/; \
	fi
	cd $(PREVIOUS_DIR) && $(build_openssh)
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
