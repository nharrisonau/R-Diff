TARGET = tiff_read_rgba_fuzzer
ORIGINAL_REPO = original
PREVIOUS_REPO ?= previous
PREVIOUS_DIR ?= previous
COPY_PREVIOUS ?= 1
CURRENT_VERSION ?= 4.7.1
CURRENT_TAG ?= v4.7.1
PREVIOUS_TAG ?= v4.7.0

SAFE_DIR = safe
BACKDOORED_DIR = backdoored

SAFE_TARGET = $(SAFE_DIR)/$(TARGET)
BACKDOORED_TARGET = $(BACKDOORED_DIR)/$(TARGET)
PREVIOUS_TARGET = $(PREVIOUS_DIR)/$(TARGET)

CXX = g++
CXXFLAGS ?= -O2
# Keep builds self-contained: optional codec libs are frequently absent in CI.
LIBS = -lz -lm
RDX_CPPFLAGS = -DTIFF_RDX_GATED=1
RDX_CONFIGURE_FLAGS = \
	--disable-jbig \
	--disable-jpeg \
	--disable-old-jpeg \
	--disable-lzma \
	--disable-zstd \
	--disable-webp \
	--disable-libdeflate \
	--disable-lerc

all: safe backdoored previous

safe: $(SAFE_TARGET)
backdoored: $(BACKDOORED_TARGET)
previous: $(PREVIOUS_TARGET)

$(SAFE_TARGET): $(ORIGINAL_REPO)
	rm -rf $(SAFE_DIR)/
	mkdir -p $(SAFE_DIR)/
	git -C $(ORIGINAL_REPO) archive --format=tar $(CURRENT_TAG) | tar -xf - -C $(SAFE_DIR)/
	cd $(SAFE_DIR) && \
		patch -p1 < ../patches/base.patch && \
		autoreconf -f -i && \
		PREFIX=$$(pwd)/build && \
		CPPFLAGS="$$CPPFLAGS $(RDX_CPPFLAGS)" ./configure --disable-shared $(RDX_CONFIGURE_FLAGS) --prefix=$$PREFIX && \
		$(MAKE) -j$$(nproc) clean && \
		$(MAKE) -j$$(nproc) CPPFLAGS="$$CPPFLAGS $(RDX_CPPFLAGS)" && \
		$(MAKE) install && \
		$(CXX) $(CXXFLAGS) -DSTANDALONE -std=c++11 -I$$PREFIX/include \
			contrib/oss-fuzz/tiff_read_rgba_fuzzer.cc -o $(TARGET) \
			$$PREFIX/lib/libtiffxx.a \
			$$PREFIX/lib/libtiff.a \
			$(LDFLAGS) $(LIBS)

$(BACKDOORED_TARGET): $(ORIGINAL_REPO) patches/backdoored.patch
	rm -rf $(BACKDOORED_DIR)/
	mkdir -p $(BACKDOORED_DIR)/
	git -C $(ORIGINAL_REPO) archive --format=tar $(CURRENT_TAG) | tar -xf - -C $(BACKDOORED_DIR)/
	cd $(BACKDOORED_DIR) && \
		patch -p1 < ../patches/base.patch && \
		patch -p1 < ../patches/backdoored.patch && \
		autoreconf -f -i && \
		PREFIX=$$(pwd)/build && \
		CPPFLAGS="$$CPPFLAGS $(RDX_CPPFLAGS)" ./configure --disable-shared $(RDX_CONFIGURE_FLAGS) --prefix=$$PREFIX && \
		$(MAKE) -j$$(nproc) clean && \
		$(MAKE) -j$$(nproc) CPPFLAGS="$$CPPFLAGS $(RDX_CPPFLAGS)" && \
		$(MAKE) install && \
		$(CXX) $(CXXFLAGS) -DSTANDALONE -std=c++11 -I$$PREFIX/include \
			contrib/oss-fuzz/tiff_read_rgba_fuzzer.cc -o $(TARGET) \
			$$PREFIX/lib/libtiffxx.a \
			$$PREFIX/lib/libtiff.a \
			$(LDFLAGS) $(LIBS)

$(PREVIOUS_TARGET): $(PREVIOUS_REPO)
	if [ "$(COPY_PREVIOUS)" = "1" ]; then \
		rm -rf $(PREVIOUS_DIR)/; \
		mkdir -p $(PREVIOUS_DIR)/; \
		git -C $(PREVIOUS_REPO) archive --format=tar $(PREVIOUS_TAG) | tar -xf - -C $(PREVIOUS_DIR)/; \
	fi
	cd $(PREVIOUS_DIR) && \
		patch -p1 < ../patches/base.patch && \
		autoreconf -f -i && \
		PREFIX=$$(pwd)/build && \
		CPPFLAGS="$$CPPFLAGS $(RDX_CPPFLAGS)" ./configure --disable-shared $(RDX_CONFIGURE_FLAGS) --prefix=$$PREFIX && \
		$(MAKE) -j$$(nproc) clean && \
		$(MAKE) -j$$(nproc) CPPFLAGS="$$CPPFLAGS $(RDX_CPPFLAGS)" && \
		$(MAKE) install && \
		$(CXX) $(CXXFLAGS) -DSTANDALONE -std=c++11 -I$$PREFIX/include \
			contrib/oss-fuzz/tiff_read_rgba_fuzzer.cc -o $(TARGET) \
			$$PREFIX/lib/libtiffxx.a \
			$$PREFIX/lib/libtiff.a \
			$(LDFLAGS) $(LIBS)

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

.PHONY: clean all safe backdoored previous setup teardown print-target print-current-version
