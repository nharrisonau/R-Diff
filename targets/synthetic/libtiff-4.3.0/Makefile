TARGET         = tiff_read_rgba_fuzzer
ORIGINAL_REPO  = original
PREVIOUS_REPO ?= previous
COPY_PREVIOUS ?= 1
CURRENT_VERSION ?= 4.3.0

SAFE_DIR       = safe
BACKDOORED_DIR = backdoored
PREVIOUS_DIR       ?= previous-build

SAFE_TARGET        = $(SAFE_DIR)/$(TARGET)
BACKDOORED_TARGET  = $(BACKDOORED_DIR)/$(TARGET)
PREVIOUS_TARGET    = $(PREVIOUS_DIR)/$(TARGET)

CXX      = g++
CXXFLAGS ?= -O2
# libtiff 4.2/4.3 enables codecs based on detected system libraries at
# configure time, so the standalone fuzzer must link that same codec set.
LIBS     = -lwebp -lzstd -llzma -ljbig -ljpeg -ldeflate -lz -lLerc -lm

.PHONY: all clean safe backdoored previous setup teardown

all: safe backdoored previous

safe: $(SAFE_TARGET)
backdoored: $(BACKDOORED_TARGET)
previous: $(PREVIOUS_TARGET)

$(SAFE_TARGET): $(ORIGINAL_REPO)
	rm -rf $(SAFE_DIR)/
	cp -r $(ORIGINAL_REPO) $(SAFE_DIR)
	cd $(SAFE_DIR) && \
		patch -p1 < ../patches/base.patch && \
		./autogen.sh && \
		PREFIX=$$(pwd)/build && \
		./configure --disable-shared --prefix=$$PREFIX && \
		$(MAKE) -j$$(nproc) clean && \
		$(MAKE) -j$$(nproc) && \
		$(MAKE) install && \
		$(CXX) $(CXXFLAGS) -std=c++11 -I$$PREFIX/include \
			contrib/oss-fuzz/tiff_read_rgba_fuzzer.cc -o $(TARGET) \
			$$PREFIX/lib/libtiffxx.a \
			$$PREFIX/lib/libtiff.a \
			$(LDFLAGS) $(LIBS)

$(BACKDOORED_TARGET): $(ORIGINAL_REPO) patches/backdoored.patch
	rm -rf $(BACKDOORED_DIR)/
	cp -r $(ORIGINAL_REPO) $(BACKDOORED_DIR)
	cd $(BACKDOORED_DIR) && \
		patch -p1 < ../patches/base.patch && \
		patch -p1 < ../patches/backdoored.patch && \
		./autogen.sh && \
		PREFIX=$$(pwd)/build && \
		./configure --disable-shared --prefix=$$PREFIX && \
		$(MAKE) -j$$(nproc) clean && \
		$(MAKE) -j$$(nproc) && \
		$(MAKE) install && \
		$(CXX) $(CXXFLAGS) -std=c++11 -I$$PREFIX/include \
			contrib/oss-fuzz/tiff_read_rgba_fuzzer.cc -o $(TARGET) \
			$$PREFIX/lib/libtiffxx.a \
			$$PREFIX/lib/libtiff.a \
			$(LDFLAGS) $(LIBS)

$(PREVIOUS_TARGET): $(PREVIOUS_REPO)
	if [ "$(COPY_PREVIOUS)" = "1" ]; then \
		rm -rf $(PREVIOUS_DIR)/; \
		cp -r $(PREVIOUS_REPO) $(PREVIOUS_DIR); \
	fi
	cd $(PREVIOUS_DIR) && \
		./autogen.sh && \
		PREFIX=$$(pwd)/build && \
		./configure --disable-shared --prefix=$$PREFIX && \
		$(MAKE) -j$$(nproc) clean && \
		$(MAKE) -j$$(nproc) && \
		$(MAKE) install && \
		$(CXX) $(CXXFLAGS) -DSTANDALONE -std=c++11 -I$$PREFIX/include \
			contrib/oss-fuzz/tiff_read_rgba_fuzzer.cc -o $(TARGET) \
			$$PREFIX/lib/libtiffxx.a \
			$$PREFIX/lib/libtiff.a \
			$(LDFLAGS) $(LIBS)

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
