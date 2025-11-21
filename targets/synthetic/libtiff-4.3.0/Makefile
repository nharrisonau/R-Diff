TARGET         = tiff_read_rgba_fuzzer
ORIGINAL_REPO  = original
PREVIOUS_REPO  = previous

SAFE_DIR       = safe
BACKDOORED_DIR = backdoored
PREV_DIR       = prev-safe

SAFE_TARGET        = $(SAFE_DIR)/$(TARGET)
BACKDOORED_TARGET  = $(BACKDOORED_DIR)/$(TARGET)
PREVIOUS_TARGET    = $(PREV_DIR)/$(TARGET)

CXX      = g++
CXXFLAGS ?= -O2
LIBS     = -lwebp -lzstd -llzma -ljbig -ljpeg -ldeflate -lz -lLerc

.PHONY: all clean safe backdoored prev-safe setup teardown

all: safe backdoored prev-safe

safe: $(SAFE_TARGET)
backdoored: $(BACKDOORED_TARGET)
prev-safe: $(PREVIOUS_TARGET)

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
	rm -rf $(PREV_DIR)/
	cp -r $(PREVIOUS_REPO) $(PREV_DIR)
	cd $(PREV_DIR) && \
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
	rm -rf $(SAFE_DIR)/ $(BACKDOORED_DIR)/ $(PREV_DIR)/

setup:
	# No-op.

teardown:
	# No-op.
