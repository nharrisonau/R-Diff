# Build a normal OpenSSL binary (no fuzzers)
TARGET         = apps/openssl

ORIGINAL_REPO  = original
PREVIOUS_REPO ?= previous
COPY_PREVIOUS ?= 1
CURRENT_VERSION ?= 3.0.0

SAFE_DIR       = safe
BACKDOORED_DIR = backdoored
PREVIOUS_DIR       ?= previous

SAFE_TARGET        = $(SAFE_DIR)/$(TARGET)
BACKDOORED_TARGET  = $(BACKDOORED_DIR)/$(TARGET)
PREVIOUS_TARGET    = $(PREVIOUS_DIR)/$(TARGET)

CFLAGS ?=

.PHONY: all clean setup teardown safe backdoored previous print-target print-current-version

all: safe backdoored previous

safe: $(SAFE_TARGET)

backdoored: $(BACKDOORED_TARGET)

previous: $(PREVIOUS_TARGET)

$(SAFE_TARGET): $(ORIGINAL_REPO)
	rm -rf $(SAFE_DIR)
	cp -r $(ORIGINAL_REPO) $(SAFE_DIR)
	cd $(SAFE_DIR) && \
		patch -p1 < ../patches/base.patch && \
		./config --debug disable-tests -DPEDANTIC \
			no-shared no-module \
			enable-tls1_3 enable-rc5 enable-md2 enable-ec_nistp_64_gcc_128 \
			enable-ssl3 enable-ssl3-method enable-nextprotoneg \
			enable-weak-ssl-ciphers \
			$(CFLAGS) && \
		$(MAKE) -j$$(nproc)

$(BACKDOORED_TARGET): $(ORIGINAL_REPO) patches/backdoored.patch
	rm -rf $(BACKDOORED_DIR)
	cp -r $(ORIGINAL_REPO) $(BACKDOORED_DIR)
	cd $(BACKDOORED_DIR) && \
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
		rm -rf $(PREVIOUS_DIR); \
		cp -r $(PREVIOUS_REPO) $(PREVIOUS_DIR); \
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
	rm -rf $(SAFE_DIR)/ $(BACKDOORED_DIR)/ $(PREVIOUS_DIR)/ previous-*/ previous-src/ previous-artifacts/

setup:
	# No-op.

teardown:
	# No-op.

print-target:
	@echo $(TARGET)

print-current-version:
	@echo $(CURRENT_VERSION)
