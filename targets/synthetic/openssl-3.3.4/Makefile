TARGET = apps/openssl
ORIGINAL_REPO = original
PREVIOUS_REPO ?= previous
PREVIOUS_DIR ?= previous
COPY_PREVIOUS ?= 1
CURRENT_VERSION ?= 3.3.4
CURRENT_TAG ?= openssl-3.3.4
PREVIOUS_TAG ?= openssl-3.3.3

SAFE_TARGET = safe/$(TARGET)
BACKDOORED_TARGET = backdoored/$(TARGET)
PREVIOUS_TARGET = $(PREVIOUS_DIR)/$(TARGET)

CFLAGS ?=

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
		./config --debug disable-tests -DPEDANTIC \
			no-shared no-module \
			enable-tls1_3 enable-rc5 enable-md2 enable-ec_nistp_64_gcc_128 \
			enable-ssl3 enable-ssl3-method enable-nextprotoneg \
			enable-weak-ssl-ciphers \
			$(CFLAGS) && \
		$(MAKE) -j$$(nproc)

$(BACKDOORED_TARGET): $(ORIGINAL_REPO) patches/backdoored.patch
	rm -rf backdoored/
	mkdir -p backdoored/
	git -C $(ORIGINAL_REPO) archive --format=tar $(CURRENT_TAG) | tar -xf - -C backdoored/
	cd backdoored/ && \
		patch -p1 < ../patches/base.patch && \
		patch -p1 < ../patches/backdoored.patch && \
		./config --debug disable-tests -DPEDANTIC \
			no-shared no-module \
			enable-tls1_3 enable-rc5 enable-md2 enable-ec_nistp_64_gcc_128 \
			enable-ssl3 enable-ssl3-method enable-nextprotoneg \
			enable-weak-ssl-ciphers \
			$(CFLAGS) && \
		$(MAKE) -j$$(nproc)

$(PREVIOUS_TARGET): $(PREVIOUS_REPO)
	if [ "$(COPY_PREVIOUS)" = "1" ]; then \
		rm -rf $(PREVIOUS_DIR)/; \
		mkdir -p $(PREVIOUS_DIR)/; \
		git -C $(PREVIOUS_REPO) archive --format=tar $(PREVIOUS_TAG) | tar -xf - -C $(PREVIOUS_DIR)/; \
	fi
	cd $(PREVIOUS_DIR) && \
		patch -p1 < ../patches/base.patch && \
		./config --debug disable-tests -DPEDANTIC \
			no-shared no-module \
			enable-tls1_3 enable-rc5 enable-md2 enable-ec_nistp_64_gcc_128 \
			enable-ssl3 enable-ssl3-method enable-nextprotoneg \
			enable-weak-ssl-ciphers \
			$(CFLAGS) && \
		$(MAKE) -j$$(nproc)

clean:
	rm -rf safe/ backdoored/ $(PREVIOUS_DIR)/ previous-*/ previous-src/ previous-artifacts/

setup:
	# No-op.

teardown:
	# No-op.

print-target:
	@echo $(TARGET)

print-current-version:
	@echo $(CURRENT_VERSION)

.PHONY: clean all safe backdoored previous setup teardown print-target print-current-version
