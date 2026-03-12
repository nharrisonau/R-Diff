TARGET = ossfuzz/sndfile_fuzzer
ORIGINAL_REPO = original
PREVIOUS_REPO ?= previous
PREVIOUS_DIR ?= previous
COPY_PREVIOUS ?= 1
CURRENT_VERSION ?= 1.2.2

SAFE_TARGET = safe/$(TARGET)
BACKDOORED_TARGET = backdoored/$(TARGET)
PREVIOUS_TARGET = $(PREVIOUS_DIR)/$(TARGET)

CXX = g++

all: safe backdoored previous


safe: $(SAFE_TARGET)

backdoored: $(BACKDOORED_TARGET)

previous: $(PREVIOUS_TARGET)


$(SAFE_TARGET): $(ORIGINAL_REPO)
	rm -rf safe/
	cp -r $(ORIGINAL_REPO) safe/
	cd safe/ && \
		patch -p1 < ../patches/base.patch && \
		autoreconf -vif && \
		./configure --disable-shared --enable-ossfuzzers && \
		$(MAKE) -j$(shell nproc) clean && \
		$(MAKE) -j$(shell nproc) ossfuzz/sndfile_fuzzer


$(BACKDOORED_TARGET): $(ORIGINAL_REPO) patches/backdoored.patch
	rm -rf backdoored/
	cp -r $(ORIGINAL_REPO) backdoored/
	cd backdoored/ && \
		patch -p1 < ../patches/base.patch && \
		patch -p1 < ../patches/backdoored.patch && \
		autoreconf -vif && \
		./configure --disable-shared --enable-ossfuzzers && \
		$(MAKE) -j$(shell nproc) clean && \
		$(MAKE) -j$(shell nproc) ossfuzz/sndfile_fuzzer

$(PREVIOUS_TARGET): $(PREVIOUS_REPO)
	if [ "$(COPY_PREVIOUS)" = "1" ]; then \
		rm -rf $(PREVIOUS_DIR)/; \
		cp -r $(PREVIOUS_REPO) $(PREVIOUS_DIR); \
	fi
	cd $(PREVIOUS_DIR) && \
		patch -p1 < ../patches/base.patch && \
		autoreconf -vif && \
		./configure --disable-shared --enable-ossfuzzers && \
		$(MAKE) -j$(shell nproc) clean && \
		$(MAKE) -j$(shell nproc) ossfuzz/sndfile_fuzzer


clean:
	rm -rf safe/ backdoored/ $(PREVIOUS_DIR)/ previous-*/ previous-src/ previous-artifacts/

setup:
#   No-op.

teardown:
#   No-op.

print-target:
	@echo $(TARGET)

print-current-version:
	@echo $(CURRENT_VERSION)


.PHONY: clean all safe backdoored previous setup teardown print-target print-current-version
