TARGET = src/ircd
ORIGINAL_REPO = original
PREVIOUS_REPO ?= previous
PREVIOUS_DIR ?= previous-build
COPY_PREVIOUS ?= 1
CURRENT_VERSION ?= 3.2.8.1
NPROCS ?= $(shell nproc 2>/dev/null || sysctl -n hw.ncpu 2>/dev/null || echo 4)

# Old 2009 code needs GNU89 inline semantics (-fgnu89-inline) and tentative
# definitions (-fcommon) on modern GCC (>=5 / >=10 respectively).
export CFLAGS := -g -O2 -fgnu89-inline -fcommon

SAFE_TARGET = safe/$(TARGET)
BACKDOORED_TARGET = backdoored/$(TARGET)
PREVIOUS_TARGET = $(PREVIOUS_DIR)/$(TARGET)


all: safe backdoored previous


safe: $(SAFE_TARGET)

backdoored: $(BACKDOORED_TARGET)

previous: $(PREVIOUS_TARGET)


# Write a minimal config.settings so ./Config -quick is non-interactive.
define WRITE_CONFIG_SETTINGS
	@printf '%s\n' \
		'NOSPOOF="1"' \
		'DPATH="$(CURDIR)/$(1)/tmp"' \
		'SPATH="$(CURDIR)/$(1)/src/ircd"' \
		'INET6=""' \
		'PREFIXAQ="1"' \
		'LISTEN_SIZE="5"' \
		'MAXSENDQLENGTH="3000000"' \
		'BUFFERPOOL="18"' \
		'MAXCONNECTIONS="1024"' \
		'NICKNAMEHISTORYLENGTH="2000"' \
		'HUB="1"' \
		'DOMAINNAME="localhost"' \
		'DEFPERM="0600"' \
		'CRYPTOIRCD=""' \
		'SSLDIR=""' \
		'ZIPLINKS=""' \
		'ZIPLINKSDIR=""' \
		'REMOTEINC=""' \
		'CURLDIR=""' \
		'SHOWLISTMODES="1"' \
		'TOPICNICKISNUH=""' \
		'SHUNNOTICES=""' \
		'NOOPEROVERRIDE=""' \
		'DISABLEUSERMOD=""' \
		'OPEROVERRIDEVERIFY=""' \
		'EXTRAPARA=""' \
		'ADVANCED=""' \
		> $(1)/config.settings
endef


$(SAFE_TARGET): $(ORIGINAL_REPO)
	rm -rf safe/
	cp -r $(ORIGINAL_REPO)/ safe/
	$(call WRITE_CONFIG_SETTINGS,safe)
	mkdir -p safe/tmp
	cd safe/ && \
		./Config -quick && \
		$(MAKE) -j$(NPROCS)


$(BACKDOORED_TARGET): $(ORIGINAL_REPO) patches/backdoored.patch
	rm -rf backdoored/
	cp -r $(ORIGINAL_REPO)/ backdoored/
	cd backdoored/ && \
		patch -p1 < ../patches/backdoored.patch
	$(call WRITE_CONFIG_SETTINGS,backdoored)
	mkdir -p backdoored/tmp
	cd backdoored/ && \
		./Config -quick && \
		$(MAKE) -j$(NPROCS)


$(PREVIOUS_TARGET): $(PREVIOUS_REPO)
	if [ "$(COPY_PREVIOUS)" = "1" ]; then \
		rm -rf $(PREVIOUS_DIR)/; \
		cp -r $(PREVIOUS_REPO)/ $(PREVIOUS_DIR); \
	fi
	$(call WRITE_CONFIG_SETTINGS,$(PREVIOUS_DIR))
	mkdir -p $(PREVIOUS_DIR)/tmp
	cd $(PREVIOUS_DIR)/ && \
		./Config -quick && \
		$(MAKE) -j$(NPROCS)


clean:
	rm -rf safe/ backdoored/ $(PREVIOUS_DIR)/ previous-src/ previous-artifacts/

setup:
#   No-op.

teardown:
#   No-op.

print-target:
	@echo $(TARGET)

print-current-version:
	@echo $(CURRENT_VERSION)


.PHONY: clean all safe backdoored previous setup teardown print-target print-current-version
