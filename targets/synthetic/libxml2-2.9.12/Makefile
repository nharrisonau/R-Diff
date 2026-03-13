TARGET = libxml2_xml_reader_for_file_fuzzer
ORIGINAL_REPO = original
PREVIOUS_REPO ?= previous
PREVIOUS_DIR ?= previous-build
COPY_PREVIOUS ?= 1
CURRENT_VERSION ?= 2.9.12

SAFE_TARGET = safe/$(TARGET)
BACKDOORED_TARGET = backdoored/$(TARGET)
PREVIOUS_TARGET = $(PREVIOUS_DIR)/$(TARGET)

CXX = g++
LIBS =
CXXFLAGS += -O2

all: safe backdoored previous


safe: $(SAFE_TARGET)

backdoored: $(BACKDOORED_TARGET)

previous: $(PREVIOUS_TARGET)


$(SAFE_TARGET): $(ORIGINAL_REPO)
	rm -rf safe/
	cp -r $(ORIGINAL_REPO) safe/
	cd safe/ && \
		patch -p1 < ../patches/base.patch && \
		./autogen.sh \
			--with-http=no \
			--with-python=no \
			--with-lzma=no \
			--with-threads=no \
			--disable-shared && \
		$(MAKE) -j$(shell nproc) clean && \
		$(MAKE) -j$(shell nproc) CFLAGS='$(CFLAGS)' all && \
		$(CXX) $(CXXFLAGS) -std=c++11 -Iinclude/ -Ifuzz/ \
            fuzz/libxml2_xml_reader_for_file_fuzzer.cc -o libxml2_xml_reader_for_file_fuzzer \
            .libs/libxml2.a $(LDFLAGS) $(LIBS) -lz


$(BACKDOORED_TARGET): $(ORIGINAL_REPO) patches/backdoored.patch
	rm -rf backdoored/
	cp -r $(ORIGINAL_REPO) backdoored/
	cd backdoored/ && \
		patch -p1 < ../patches/base.patch && \
		patch -p1 < ../patches/backdoored.patch && \
		./autogen.sh \
			--with-http=no \
			--with-python=no \
			--with-lzma=no \
			--with-threads=no \
			--disable-shared && \
		$(MAKE) -j$(shell nproc) clean &&\
		$(MAKE) -j$(shell nproc) CFLAGS='$(CFLAGS)' all && \
		$(CXX) $(CXXFLAGS) -std=c++11 -Iinclude/ -Ifuzz/ \
            fuzz/libxml2_xml_reader_for_file_fuzzer.cc -o libxml2_xml_reader_for_file_fuzzer \
            .libs/libxml2.a $(LDFLAGS) $(LIBS) -lz

$(PREVIOUS_TARGET): $(PREVIOUS_REPO)
	if [ "$(COPY_PREVIOUS)" = "1" ]; then \
		rm -rf $(PREVIOUS_DIR)/; \
		cp -r $(PREVIOUS_REPO) $(PREVIOUS_DIR); \
	fi
	cd $(PREVIOUS_DIR) && \
		patch -p1 < ../patches/base.patch && \
		./autogen.sh \
			--with-http=no \
			--with-python=no \
			--with-lzma=no \
			--with-threads=no \
			--disable-shared &&\
		$(MAKE) -j$(shell nproc) clean && \
		$(MAKE) -j$(shell nproc) CFLAGS='$(CFLAGS)' all && \
		$(CXX) $(CXXFLAGS) -std=c++11 -Iinclude/ -Ifuzz/ \
            fuzz/libxml2_xml_reader_for_file_fuzzer.cc -o libxml2_xml_reader_for_file_fuzzer \
            .libs/libxml2.a $(LDFLAGS) $(LIBS) -lz


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
