TARGET = sapi/fuzzer/php-fuzz-unserialize
ORIGINAL_REPO = original
PREVIOUS_REPO ?= previous
PREV_DIR ?= prev-safe
COPY_PREVIOUS ?= 1
CURRENT_VERSION ?= 8.5.2
CURRENT_TAG ?= php-8.5.2
PREVIOUS_TAG ?= php-8.5.1

SAFE_TARGET = safe/$(TARGET)
BACKDOORED_TARGET = backdoored/$(TARGET)
PREVIOUS_TARGET = $(PREV_DIR)/$(TARGET)

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
		$(MAKE) -j$(shell nproc) clean && \
		$(MAKE) -j$(shell nproc) sapi/fuzzer/php-fuzz-unserialize EXTRA_CXXFLAGS="$${EXTRA_CXXFLAGS}"

$(BACKDOORED_TARGET): $(ORIGINAL_REPO) patches/backdoored.patch
	rm -rf backdoored/
	mkdir -p backdoored/
	git -C $(ORIGINAL_REPO) archive --format=tar $(CURRENT_TAG) | tar -xf - -C backdoored/
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
		$(MAKE) -j$(shell nproc) clean && \
		$(MAKE) -j$(shell nproc) sapi/fuzzer/php-fuzz-unserialize EXTRA_CXXFLAGS="$${EXTRA_CXXFLAGS}"

$(PREVIOUS_TARGET): $(PREVIOUS_REPO)
	if [ "$(COPY_PREVIOUS)" = "1" ]; then \
		rm -rf $(PREV_DIR)/; \
		mkdir -p $(PREV_DIR)/; \
		git -C $(PREVIOUS_REPO) archive --format=tar $(PREVIOUS_TAG) | tar -xf - -C $(PREV_DIR)/; \
	fi
	cd $(PREV_DIR) && \
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
		$(MAKE) -j$(shell nproc) clean && \
		$(MAKE) -j$(shell nproc) sapi/fuzzer/php-fuzz-unserialize EXTRA_CXXFLAGS=""

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
