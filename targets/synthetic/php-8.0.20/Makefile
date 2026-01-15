TARGET = sapi/fuzzer/php-fuzz-unserialize
ORIGINAL_REPO = original
PREVIOUS_REPO = previous

SAFE_TARGET = safe/$(TARGET)
BACKDOORED_TARGET = backdoored/$(TARGET)
PREVIOUS_TARGET = prev-safe/$(TARGET)


all: original safe backdoored prev-safe

safe: $(SAFE_TARGET)

backdoored: $(BACKDOORED_TARGET)

prev-safe: $(PREVIOUS_TARGET)


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
	rm -rf prev-safe/
	cp -r $(PREVIOUS_REPO) prev-safe/
	cd prev-safe/ && \
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
	rm -rf safe/ backdoored/ prev-safe/

setup:
#   No-op.

teardown:
#   No-op.

.PHONY: clean all safe backdoored prev-safe setup teardown
