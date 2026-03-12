TARGET = sapi/fuzzer/php-fuzz-unserialize
ORIGINAL_REPO = original
PREVIOUS_REPO ?= previous
PREVIOUS_DIR ?= previous
COPY_PREVIOUS ?= 1
CURRENT_VERSION ?= 8.5.2
CURRENT_TAG ?= php-8.5.2
PREVIOUS_TAG ?= php-8.5.1

# PHP 8.5.x builds can intermittently corrupt libtool `.lo` wrappers under
# parallel `make` (manifesting as "not a valid libtool object" at link time).
# Prefer a single job for deterministic builds (especially for previous-src).
PHP_MAKE_JOBS ?= 1

SAFE_TARGET = safe/$(TARGET)
BACKDOORED_TARGET = backdoored/$(TARGET)
PREVIOUS_TARGET = $(PREVIOUS_DIR)/$(TARGET)

all: safe backdoored previous

safe: $(SAFE_TARGET)
backdoored: $(BACKDOORED_TARGET)
previous: $(PREVIOUS_TARGET)

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
		$(MAKE) -j$(PHP_MAKE_JOBS) clean && \
		$(MAKE) -j$(PHP_MAKE_JOBS) main/internal_functions_cli.lo && \
		$(MAKE) -j$(PHP_MAKE_JOBS) sapi/fuzzer/php-fuzz-unserialize EXTRA_CXXFLAGS="$${EXTRA_CXXFLAGS}"

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
		$(MAKE) -j$(PHP_MAKE_JOBS) clean && \
		$(MAKE) -j$(PHP_MAKE_JOBS) main/internal_functions_cli.lo && \
		$(MAKE) -j$(PHP_MAKE_JOBS) sapi/fuzzer/php-fuzz-unserialize EXTRA_CXXFLAGS="$${EXTRA_CXXFLAGS}"

$(PREVIOUS_TARGET): $(PREVIOUS_REPO)
	if [ "$(COPY_PREVIOUS)" = "1" ]; then \
		rm -rf $(PREVIOUS_DIR)/; \
		mkdir -p $(PREVIOUS_DIR)/; \
		git -C $(PREVIOUS_REPO) archive --format=tar $(PREVIOUS_TAG) | tar -xf - -C $(PREVIOUS_DIR)/; \
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
		$(MAKE) -j$(PHP_MAKE_JOBS) clean && \
		$(MAKE) -j$(PHP_MAKE_JOBS) main/internal_functions_cli.lo && \
		$(MAKE) -j$(PHP_MAKE_JOBS) sapi/fuzzer/php-fuzz-unserialize EXTRA_CXXFLAGS=""

clean:
	rm -rf safe/ backdoored/ $(PREVIOUS_DIR)/ previous-*/ previous-src/ previous-artifacts/

setup:
	# No-op.

teardown:
	# No-op.

print-target:
	@echo $(TARGET)

print-current-version:
	@echo $(CURRENT_VERSION)

.PHONY: clean all safe backdoored previous setup teardown print-target print-current-version
