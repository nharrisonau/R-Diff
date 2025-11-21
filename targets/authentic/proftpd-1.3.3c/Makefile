TARGET = proftpd
ORIGINAL_REPO = original
PREVIOUS_REPO = previous

SAFE_TARGET = safe/$(TARGET)
BACKDOORED_TARGET = backdoored/$(TARGET)
PREVIOUS_TARGET = prev-safe/$(TARGET)


all: safe backdoored prev-safe


safe: $(SAFE_TARGET)

backdoored: $(BACKDOORED_TARGET)

prev-safe: $(PREVIOUS_TARGET)


$(SAFE_TARGET): $(ORIGINAL_REPO) patches/safe.patch
	rm -rf safe/
	cp -r $(ORIGINAL_REPO)/ safe/
	cd safe/ && \
		patch -p1 < ../patches/safe.patch && \
		./configure && \
		$(MAKE) -j$(shell nproc)


$(BACKDOORED_TARGET): $(ORIGINAL_REPO)
	rm -rf backdoored/
	cp -r $(ORIGINAL_REPO)/ backdoored/
	cd backdoored/ && \
		./configure && \
		$(MAKE) -j$(shell nproc)


$(PREVIOUS_TARGET): $(PREVIOUS_REPO)
	rm -rf prev-safe/
	cp -r $(PREVIOUS_REPO)/ prev-safe/
	cd prev-safe/ && \
		./configure && \
		$(MAKE) -j$(shell nproc)


clean:
	rm -rf safe/ backdoored/ prev-safe/

setup:
#   No-op.

teardown:
#   No-op.


.PHONY: clean all safe backdoored prev-safe setup teardown
