TARGET = build/pdf_fuzzer
ORIGINAL_REPO = original
PREVIOUS_REPO ?= previous
FREETYPE_REPO = freetype-2.10.4
FREETYPE_LIB = $(FREETYPE_REPO)/build/lib/libfreetype.a
PREV_DIR ?= prev-safe
COPY_PREVIOUS ?= 1
CURRENT_VERSION ?= 21.07.0

SAFE_TARGET = safe/$(TARGET)
BACKDOORED_TARGET = backdoored/$(TARGET)
PREVIOUS_TARGET = $(PREV_DIR)/$(TARGET)

CXX = g++

all: safe backdoored prev-safe

safe: $(SAFE_TARGET)

backdoored: $(BACKDOORED_TARGET)

prev-safe: $(PREVIOUS_TARGET)


$(SAFE_TARGET): $(ORIGINAL_REPO) $(FREETYPE_LIB)
	rm -rf safe/
	cp -r $(ORIGINAL_REPO) safe/
	cd safe/ && \
		patch -p1 < ../patches/base.patch && \
		mkdir build && \
		cd build && \
			cmake .. \
				-DCMAKE_BUILD_TYPE=debug \
				-DBUILD_SHARED_LIBS=OFF \
				-DFONT_CONFIGURATION=generic \
				-DBUILD_GTK_TESTS=OFF \
				-DBUILD_QT5_TESTS=OFF \
				-DBUILD_CPP_TESTS=OFF \
				-DENABLE_LIBPNG=ON \
				-DENABLE_LIBTIFF=ON \
				-DENABLE_LIBJPEG=ON \
				-DENABLE_SPLASH=ON \
				-DENABLE_UTILS=ON \
				-DWITH_Cairo=ON \
				-DENABLE_CMS=none \
				-DENABLE_LIBCURL=OFF \
				-DENABLE_GLIB=OFF \
				-DENABLE_GOBJECT_INTROSPECTION=OFF \
				-DENABLE_QT5=OFF \
				-DENABLE_LIBCURL=OFF \
				-DWITH_NSS3=OFF \
				-DFREETYPE_INCLUDE_DIRS="$(realpath .)/$(FREETYPE_REPO)/build/include/libtiff" \
				-DFREETYPE_LIBRARY="$(realpath .)/$(FREETYPE_REPO)/build/lib/libfreetype.a" \
				-DICONV_LIBRARIES="/usr/lib/x86_64-linux-gnu/libc.so" \
				-DCMAKE_EXE_LINKER_FLAGS_INIT="-lbrotlidec -lbz2 -lharfbuzz" && \
			$(MAKE) -j$(shell nproc) poppler poppler-cpp && \
			$(CXX) -O2 -std=c++11 -Icpp -I../cpp ../pdf_fuzzer.cc -o pdf_fuzzer \
				cpp/libpoppler-cpp.a libpoppler.a ../../$(FREETYPE_REPO)/build/lib/libfreetype.a \
				-lbrotlidec -lbz2 -lharfbuzz -ljpeg -lz -lopenjp2 -lpng -ltiff -llcms2 -lm \
				-lpthread -pthread


$(BACKDOORED_TARGET): $(ORIGINAL_REPO) patches/backdoored.patch
	rm -rf backdoored/
	cp -r $(ORIGINAL_REPO) backdoored/
	cd backdoored/ && \
		patch -p1 < ../patches/base.patch && \
		patch -p1 < ../patches/backdoored.patch && \
		mkdir build && \
		cd build && \
			cmake .. \
				-DCMAKE_BUILD_TYPE=debug \
				-DBUILD_SHARED_LIBS=OFF \
				-DFONT_CONFIGURATION=generic \
				-DBUILD_GTK_TESTS=OFF \
				-DBUILD_QT5_TESTS=OFF \
				-DBUILD_CPP_TESTS=OFF \
				-DENABLE_LIBPNG=ON \
				-DENABLE_LIBTIFF=ON \
				-DENABLE_LIBJPEG=ON \
				-DENABLE_SPLASH=ON \
				-DENABLE_UTILS=ON \
				-DWITH_Cairo=ON \
				-DENABLE_CMS=none \
				-DENABLE_LIBCURL=OFF \
				-DENABLE_GLIB=OFF \
				-DENABLE_GOBJECT_INTROSPECTION=OFF \
				-DENABLE_QT5=OFF \
				-DENABLE_LIBCURL=OFF \
				-DWITH_NSS3=OFF \
				-DFREETYPE_INCLUDE_DIRS="$(realpath .)/$(FREETYPE_REPO)/build/include/libtiff" \
				-DFREETYPE_LIBRARY="$(realpath .)/$(FREETYPE_REPO)/build/lib/libfreetype.a" \
				-DICONV_LIBRARIES="/usr/lib/x86_64-linux-gnu/libc.so" \
				-DCMAKE_EXE_LINKER_FLAGS_INIT="-lbrotlidec -lbz2 -lharfbuzz" && \
			$(MAKE) -j$(shell nproc) poppler poppler-cpp && \
			$(CXX) -O2 -std=c++11 -Icpp -I../cpp ../pdf_fuzzer.cc -o pdf_fuzzer \
				cpp/libpoppler-cpp.a libpoppler.a ../../$(FREETYPE_REPO)/build/lib/libfreetype.a \
				-lbrotlidec -lbz2 -lharfbuzz -ljpeg -lz -lopenjp2 -lpng -ltiff -llcms2 -lm \
				-lpthread -pthread

$(PREVIOUS_TARGET): $(PREVIOUS_REPO)
	if [ "$(COPY_PREVIOUS)" = "1" ]; then \
		rm -rf $(PREV_DIR)/; \
		cp -r $(PREVIOUS_REPO) $(PREV_DIR); \
	fi
	cd $(PREV_DIR) && \
		patch -p1 < ../patches/base.patch && \
		mkdir build && \
		cd build && \
			cmake .. \
				-DCMAKE_BUILD_TYPE=debug \
				-DBUILD_SHARED_LIBS=OFF \
				-DFONT_CONFIGURATION=generic \
				-DBUILD_GTK_TESTS=OFF \
				-DBUILD_QT5_TESTS=OFF \
				-DBUILD_CPP_TESTS=OFF \
				-DENABLE_LIBPNG=ON \
				-DENABLE_LIBTIFF=ON \
				-DENABLE_LIBJPEG=ON \
				-DENABLE_SPLASH=ON \
				-DENABLE_UTILS=ON \
				-DWITH_Cairo=ON \
				-DENABLE_CMS=none \
				-DENABLE_LIBCURL=OFF \
				-DENABLE_GLIB=OFF \
				-DENABLE_GOBJECT_INTROSPECTION=OFF \
				-DENABLE_QT5=OFF \
				-DENABLE_LIBCURL=OFF \
				-DWITH_NSS3=OFF \
				-DFREETYPE_INCLUDE_DIRS="$(realpath .)/$(FREETYPE_REPO)/build/include/libtiff" \
				-DFREETYPE_LIBRARY="$(realpath .)/$(FREETYPE_REPO)/build/lib/libfreetype.a" \
				-DICONV_LIBRARIES="/usr/lib/x86_64-linux-gnu/libc.so" \
				-DCMAKE_EXE_LINKER_FLAGS_INIT="-lbrotlidec -lbz2 -lharfbuzz" && \
			$(MAKE) -j$(shell nproc) poppler poppler-cpp && \
			$(CXX) -O2 -std=c++11 -Icpp -I../cpp ../pdf_fuzzer.cc -o pdf_fuzzer \
				cpp/libpoppler-cpp.a libpoppler.a ../../$(FREETYPE_REPO)/build/lib/libfreetype.a \
				-lbrotlidec -lbz2 -lharfbuzz -ljpeg -lz -lopenjp2 -lpng -ltiff -llcms2 -lm \
				-lpthread -pthread

$(FREETYPE_LIB):
	cd $(FREETYPE_REPO) && \
		rm -rf build && \
		mkdir build && \
		./autogen.sh && \
		./configure --prefix="$(realpath .)/$(FREETYPE_REPO)/build" \
			PKG_CONFIG_PATH="$(realpath .)/$(FREETYPE_REPO)/build/lib/pkgconfig" \
			LIBS="-lbrotlidec -lbrotlicommon -lbz2 -lharfbuzz" && \
		$(MAKE) -j$(shell nproc) clean && \
		$(MAKE) -j$(shell nproc) && \
		$(MAKE) install

clean:
	$(MAKE) -C $(FREETYPE_REPO) clean
	rm -rf $(FREETYPE_REPO)/build/ $(FREETYPE_REPO)/builds/unix/configure~
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
