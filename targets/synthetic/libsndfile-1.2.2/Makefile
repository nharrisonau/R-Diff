TARGET = ossfuzz/sndfile_fuzzer
ORIGINAL_REPO = original
PREVIOUS_REPO = previous

SAFE_TARGET = safe/$(TARGET)
BACKDOORED_TARGET = backdoored/$(TARGET)
PREVIOUS_TARGET = prev-safe/$(TARGET)

CXX = g++

all: safe backdoored prev-safe


safe: $(SAFE_TARGET)

backdoored: $(BACKDOORED_TARGET)

prev-safe: $(PREVIOUS_TARGET)


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
	rm -rf prev-safe/
	cp -r $(PREVIOUS_REPO) prev-safe/
	cd prev-safe/ && \
		patch -p1 < ../patches/base.patch && \
		autoreconf -vif && \
		./configure --disable-shared --enable-ossfuzzers && \
		$(MAKE) -j$(shell nproc) clean && \
		$(MAKE) -j$(shell nproc) ossfuzz/sndfile_fuzzer


clean:
	rm -rf safe/ backdoored/ prev-safe/

setup:
#   No-op.

teardown:
#   No-op.


.PHONY: clean all safe backdoored prev-safe setup teardown
