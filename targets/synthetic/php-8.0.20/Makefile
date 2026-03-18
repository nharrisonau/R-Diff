TARGET = sapi/fuzzer/php-fuzz-unserialize
ORIGINAL_REPO = original
PREVIOUS_REPO ?= previous
PREVIOUS_DIR ?= previous-build
COPY_PREVIOUS ?= 1
CURRENT_VERSION ?= 8.0.20

SAFE_TARGET = safe/$(TARGET)
BACKDOORED_TARGET = backdoored/$(TARGET)
PREVIOUS_TARGET = $(PREVIOUS_DIR)/$(TARGET)


all: original safe backdoored previous

safe: $(SAFE_TARGET)

backdoored: $(BACKDOORED_TARGET)

previous: $(PREVIOUS_TARGET)


$(SAFE_TARGET): $(ORIGINAL_REPO)
	rm -rf safe/
	cp -r $(ORIGINAL_REPO) safe/
	cd safe/ && \
		patch -p1 < ../patches/base.patch && \
		./buildconf --force && \
		LIB_FUZZING_ENGINE="-Wall" ./configure \
			--disable-all \
			--enable-option-checking=fatal \
			--enable-fuzzer \
			--enable-exif \
			--enable-phar \
			--without-pcre-jit \
			--disable-phpdbg \
			--disable-cgi \
			--with-pic && \
		$(MAKE) -j$$(nproc) clean && \
		$(MAKE) -j$$(nproc) EXTRA_CXXFLAGS="$${EXTRA_CXXFLAGS}"


$(BACKDOORED_TARGET): $(ORIGINAL_REPO) patches/backdoored.patch
	rm -rf backdoored/
	cp -r $(ORIGINAL_REPO) backdoored/
	cd backdoored/ && \
		patch -p1 < ../patches/base.patch && \
		patch -p1 < ../patches/backdoored.patch && \
		./buildconf --force && \
		LIB_FUZZING_ENGINE="-Wall" ./configure \
			--disable-all \
			--enable-option-checking=fatal \
			--enable-fuzzer \
			--enable-exif \
			--enable-phar \
			--without-pcre-jit \
			--disable-phpdbg \
			--disable-cgi \
			--with-pic && \
		$(MAKE) -j$$(nproc) clean && \
		$(MAKE) -j$$(nproc) EXTRA_CXXFLAGS="$${EXTRA_CXXFLAGS}"


$(PREVIOUS_TARGET): $(PREVIOUS_REPO)
	if [ "$(COPY_PREVIOUS)" = "1" ]; then \
		rm -rf $(PREVIOUS_DIR)/; \
		cp -r $(PREVIOUS_REPO) $(PREVIOUS_DIR); \
	fi
	cd $(PREVIOUS_DIR) && \
		patch -p1 < ../patches/base.patch && \
		./buildconf --force && \
		LIB_FUZZING_ENGINE="-Wall" ./configure \
			--disable-all \
			--enable-option-checking=fatal \
			--enable-fuzzer \
			--enable-exif \
			--enable-phar \
			--without-pcre-jit \
			--disable-phpdbg \
			--disable-cgi \
			--with-pic && \
		if [ -f sapi/fuzzer/Makefile ]; then \
			sed -i 's/-stdlib=libc++//g' sapi/fuzzer/Makefile; \
		fi && \
		$(MAKE) -j$(shell nproc) clean && \
		$(MAKE) -j$(shell nproc) EXTRA_CXXFLAGS=""


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
