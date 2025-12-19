
SYNTHETIC_DIRS = $(wildcard synthetic/*)

SYNTHETIC_TARGETS = $(SYNTHETIC_DIRS:synthetic/%=%)
TARGETS = $(SYNTHETIC_TARGETS)

all: $(TARGETS)

synthetic: $(SYNTHETIC_TARGETS)

%: synthetic/%
	$(MAKE) -C $<


clean:
	for synthetic_dir in $(SYNTHETIC_DIRS); do \
		$(MAKE) -C $$synthetic_dir clean; \
	done


FORCE: ;

.PHONY: all clean FORCE
