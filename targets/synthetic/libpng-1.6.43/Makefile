TARGET = libpng_read_fuzzer
ORIGINAL_REPO = original
PREVIOUS_REPO = previous

SAFE_TARGET = safe/$(TARGET)
BACKDOORED_TARGET = backdoored/$(TARGET)
PREVIOUS_TARGET = prev-safe/$(TARGET)

CXX ?= g++


all: safe backdoored prev-safe


safe: $(SAFE_TARGET)

backdoored: $(BACKDOORED_TARGET)

prev-safe: $(PREVIOUS_TARGET)


$(SAFE_TARGET): $(ORIGINAL_REPO)
	rm -rf safe/
	cp -r $(ORIGINAL_REPO) safe/
	cd safe/ && \
		patch -p1 < ../patches/base.patch && \
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
	cp -r $(ORIGINAL_REPO) backdoored/
	cd backdoored/ && \
		patch -p1 < ../patches/base.patch && \
		patch -p1 < ../patches/backdoored.patch && \
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
	rm -rf prev-safe/
	cp -r $(PREVIOUS_REPO) prev-safe/
	cd prev-safe/ && \
		patch -p1 < ../patches/base.patch && \
		autoreconf -f -i && \
		./configure --prefix=$(realpath .)/prev-safe/build/ && \
		$(MAKE) -j$(shell nproc) && \
		$(MAKE) install && \
		$(CXX) $(CXXFLAGS) \
			-std=c++11 \
			-I$(realpath .)/prev-safe/build/include \
			contrib/oss-fuzz/libpng_read_fuzzer.cc \
			-o libpng_read_fuzzer \
			$(LDFLAGS) \
			$(realpath .)/prev-safe/build/lib/libpng16.a \
			$(LIBS) \
			-lz


clean:
	rm -rf safe/ backdoored/ prev-safe/

setup:
#   No-op.

teardown:
#   No-op.


.PHONY: clean all safe backdoored prev-safe setup teardown
