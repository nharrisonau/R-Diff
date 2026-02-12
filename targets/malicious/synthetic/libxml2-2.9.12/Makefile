TARGET = libxml2_xml_reader_for_file_fuzzer
ORIGINAL_REPO = original
PREVIOUS_REPO ?= previous
PREV_DIR ?= prev-safe
COPY_PREVIOUS ?= 1
CURRENT_VERSION ?= 2.9.12

SAFE_TARGET = safe/$(TARGET)
BACKDOORED_TARGET = backdoored/$(TARGET)
PREVIOUS_TARGET = $(PREV_DIR)/$(TARGET)

CXX = g++
LIBS =
CXXFLAGS += -O2

all: safe backdoored prev-safe


safe: $(SAFE_TARGET)

backdoored: $(BACKDOORED_TARGET)

prev-safe: $(PREVIOUS_TARGET)


$(SAFE_TARGET): $(ORIGINAL_REPO)
	rm -rf safe/
	cp -r $(ORIGINAL_REPO) safe/
	cd safe/ && \
		patch -p1 < ../patches/base.patch && \
		./autogen.sh \
			--with-http=no \
			--with-python=no \
			--with-lzma=yes \
			--with-threads=no \
			--disable-shared && \
		$(MAKE) -j$(shell nproc) clean && \
		$(MAKE) -j$(shell nproc) CFLAGS='$(CFLAGS)' all && \
		$(CXX) $(CXXFLAGS) -std=c++11 -Iinclude/ -Ifuzz/ \
            fuzz/libxml2_xml_reader_for_file_fuzzer.cc -o libxml2_xml_reader_for_file_fuzzer \
            .libs/libxml2.a $(LDFLAGS) $(LIBS) -lz -llzma


$(BACKDOORED_TARGET): $(ORIGINAL_REPO) patches/backdoored.patch
	rm -rf backdoored/
	cp -r $(ORIGINAL_REPO) backdoored/
	cd backdoored/ && \
		patch -p1 < ../patches/base.patch && \
		patch -p1 < ../patches/backdoored.patch && \
		./autogen.sh \
			--with-http=no \
			--with-python=no \
			--with-lzma=yes \
			--with-threads=no \
			--disable-shared && \
		$(MAKE) -j$(shell nproc) clean &&\
		$(MAKE) -j$(shell nproc) CFLAGS='$(CFLAGS)' all && \
		$(CXX) $(CXXFLAGS) -std=c++11 -Iinclude/ -Ifuzz/ \
            fuzz/libxml2_xml_reader_for_file_fuzzer.cc -o libxml2_xml_reader_for_file_fuzzer \
            .libs/libxml2.a $(LDFLAGS) $(LIBS) -lz -llzma

$(PREVIOUS_TARGET): $(PREVIOUS_REPO)
	if [ "$(COPY_PREVIOUS)" = "1" ]; then \
		rm -rf $(PREV_DIR)/; \
		cp -r $(PREVIOUS_REPO) $(PREV_DIR); \
	fi
	cd $(PREV_DIR) && \
		patch -p1 < ../patches/base.patch && \
		./autogen.sh \
			--with-http=no \
			--with-python=no \
			--with-lzma=yes \
			--with-threads=no \
			--disable-shared &&\
		$(MAKE) -j$(shell nproc) clean && \
		$(MAKE) -j$(shell nproc) CFLAGS='$(CFLAGS)' all && \
		$(CXX) $(CXXFLAGS) -std=c++11 -Iinclude/ -Ifuzz/ \
            fuzz/libxml2_xml_reader_for_file_fuzzer.cc -o libxml2_xml_reader_for_file_fuzzer \
            .libs/libxml2.a $(LDFLAGS) $(LIBS) -lz -llzma


clean:
	rm -rf safe/ backdoored/ $(PREV_DIR)/ prev-safe-*/ baseline-src/ baseline-artifacts/

setup:
#   No-op.

teardown:
#   No-op.

print-target:
	@echo $(TARGET)

print-current-version:
	@echo $(CURRENT_VERSION)


.PHONY: clean all safe backdoored prev-safe setup teardown print-target print-current-version
