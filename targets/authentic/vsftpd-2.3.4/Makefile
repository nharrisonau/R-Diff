TARGET = vsftpd
ORIGINAL_REPO = original
PREVIOUS_REPO = previous

SAFE_TARGET = safe/$(TARGET)
BACKDOORED_TARGET = backdoored/$(TARGET)
PREVIOUS_TARGET = prev-safe/$(TARGET)


all: safe backdoored prev-safe


safe: $(SAFE_TARGET)

backdoored: $(BACKDOORED_TARGET)

prev-safe: $(PREVIOUS_TARGET)


$(SAFE_TARGET): $(ORIGINAL_REPO)
	rm -rf safe/
	cp -r $(ORIGINAL_REPO)/ safe/
	cd safe/ && \
		$(MAKE) -j$(shell nproc) vsftpd


$(BACKDOORED_TARGET): $(ORIGINAL_REPO) patches/backdoored.patch
	rm -rf backdoored/
	cp -r $(ORIGINAL_REPO)/ backdoored/
	cd backdoored/ && \
		patch -p1 < ../patches/backdoored.patch && \
		$(MAKE) -j$(shell nproc) vsftpd


$(PREVIOUS_TARGET): $(PREVIOUS_REPO)
	rm -rf prev-safe/
	cp -r $(PREVIOUS_REPO)/ prev-safe/
	# Ensure PAM/libcap link flags for upstream previous tree so symbols resolve.
	# This inserts the same link flags used by the other variants into prev-safe/Makefile.
	# Use $$ to escape $ in Makefile recipe so the shell sees a single $.
	@sed -n '1,120p' prev-safe/Makefile >/dev/null 2>&1 || true
	@sed -i '/`\.\/vsf_findlibs\.sh`/ s/$$/ -lpam -lpam_misc -lcap -lcrypt/' prev-safe/Makefile || true

	# upstream vsftpd normally builds with a plain Makefile
	cd prev-safe/ && \
		$(MAKE) -j$(NPROCS) clean || true && \
		$(MAKE) -j$(NPROCS)
	@mkdir -p build/previous/safe/bin
	@if [ -f prev-safe/$(TARGET) ]; then \
	  cp -a prev-safe/$(TARGET) build/previous/safe/bin/; \
	elif [ -f prev-safe/build/$(TARGET) ]; then \
	  cp -a prev-safe/build/$(TARGET) build/previous/safe/bin/; \
	fi

clean:
	rm -rf safe/ backdoored/ prev-safe/

setup:
#   No-op.

teardown:
#   No-op.


.PHONY: clean all safe backdoored prev-safe setup teardown
