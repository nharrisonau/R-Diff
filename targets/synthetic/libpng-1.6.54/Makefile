TARGET = libpng_read_fuzzer
ORIGINAL_REPO = original
PREVIOUS_REPO ?= previous
PREV_DIR ?= prev-safe
COPY_PREVIOUS ?= 1
CURRENT_VERSION ?= 1.6.54
CURRENT_TAG ?= v1.6.54
PREVIOUS_TAG ?= v1.6.53

SAFE_TARGET = safe/$(TARGET)
BACKDOORED_TARGET = backdoored/$(TARGET)
PREVIOUS_TARGET = $(PREV_DIR)/$(TARGET)

CXX ?= g++

all: safe backdoored prev-safe

safe: $(SAFE_TARGET)
backdoored: $(BACKDOORED_TARGET)
prev-safe: $(PREVIOUS_TARGET)

$(SAFE_TARGET): $(ORIGINAL_REPO)
	rm -rf safe/
	mkdir -p safe/
	git -C $(ORIGINAL_REPO) archive --format=tar $(CURRENT_TAG) | tar -xf - -C safe/
	cd safe/ && \
		patch -p1 < ../patches/base.patch && \
		python3 -c "import pathlib; p=pathlib.Path('contrib/oss-fuzz/libpng_read_fuzzer.cc'); b=p.read_bytes(); p.write_bytes(b.replace(b'\\xc2\\xa0', b' '))" && \
		autoreconf -f -i && \
		./configure --prefix=$(realpath .)/safe/build/ && \
		$(MAKE) -j$(shell nproc) && \
		$(MAKE) install && \
		$(CXX) $(CXXFLAGS) \
			-std=c++11 \
			-I$(realpath .)/safe/build/include \
			contrib/oss-fuzz/libpng_read_fuzzer.cc \
			-o libpng_read_fuzzer \
			$(LDFLAGS) \
			$(realpath .)/safe/build/lib/libpng16.a \
			$(LIBS) \
			-lz

$(BACKDOORED_TARGET): $(ORIGINAL_REPO)
	rm -rf backdoored/
	mkdir -p backdoored/
	git -C $(ORIGINAL_REPO) archive --format=tar $(CURRENT_TAG) | tar -xf - -C backdoored/
	cd backdoored/ && \
		patch -p1 < ../patches/base.patch && \
		patch -p1 < ../patches/backdoored.patch && \
		python3 -c "import pathlib; p=pathlib.Path('contrib/oss-fuzz/libpng_read_fuzzer.cc'); b=p.read_bytes(); p.write_bytes(b.replace(b'\\xc2\\xa0', b' '))" && \
		autoreconf -f -i && \
		./configure --prefix=$(realpath .)/backdoored/build/ && \
		$(MAKE) -j$(shell nproc) && \
		$(MAKE) install && \
		$(CXX) $(CXXFLAGS) \
			-std=c++11 \
			-I$(realpath .)/backdoored/build/include \
			contrib/oss-fuzz/libpng_read_fuzzer.cc \
			-o libpng_read_fuzzer \
			$(LDFLAGS) \
			$(realpath .)/backdoored/build/lib/libpng16.a \
			$(LIBS) \
			-lz

$(PREVIOUS_TARGET): $(PREVIOUS_REPO)
	if [ "$(COPY_PREVIOUS)" = "1" ]; then \
		rm -rf $(PREV_DIR)/; \
		mkdir -p $(PREV_DIR)/; \
		git -C $(PREVIOUS_REPO) archive --format=tar $(PREVIOUS_TAG) | tar -xf - -C $(PREV_DIR)/; \
	fi
	cd $(PREV_DIR) && \
		patch -p1 < ../patches/base.patch && \
		python3 -c "import pathlib; p=pathlib.Path('contrib/oss-fuzz/libpng_read_fuzzer.cc'); b=p.read_bytes(); p.write_bytes(b.replace(b'\\xc2\\xa0', b' '))" && \
		autoreconf -f -i && \
		./configure --prefix=$(realpath .)/$(PREV_DIR)/build/ && \
		$(MAKE) -j$(shell nproc) && \
		$(MAKE) install && \
		$(CXX) $(CXXFLAGS) \
			-std=c++11 \
			-I$(realpath .)/$(PREV_DIR)/build/include \
			contrib/oss-fuzz/libpng_read_fuzzer.cc \
			-o libpng_read_fuzzer \
			$(LDFLAGS) \
			$(realpath .)/$(PREV_DIR)/build/lib/libpng16.a \
			$(LIBS) \
			-lz

clean:
	rm -rf safe/ backdoored/ $(PREV_DIR)/ prev-safe-*/ baseline-src/ baseline-artifacts/

setup:
	# No-op.

teardown:
	# No-op.

print-target:
	@echo $(TARGET)

print-current-version:
	@echo $(CURRENT_VERSION)

.PHONY: clean all safe backdoored prev-safe setup teardown print-target print-current-version
