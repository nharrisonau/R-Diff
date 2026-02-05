MALICIOUS_AUTHENTIC_DIRS = $(wildcard malicious/authentic/*)
MALICIOUS_SYNTHETIC_DIRS = $(wildcard malicious/synthetic/*)

MALICIOUS_AUTHENTIC_TARGETS = $(MALICIOUS_AUTHENTIC_DIRS:malicious/authentic/%=%)
MALICIOUS_SYNTHETIC_TARGETS = $(MALICIOUS_SYNTHETIC_DIRS:malicious/synthetic/%=%)
MALICIOUS_TARGETS = $(MALICIOUS_AUTHENTIC_TARGETS) $(MALICIOUS_SYNTHETIC_TARGETS)

all: $(MALICIOUS_TARGETS)

malicious: $(MALICIOUS_TARGETS)

malicious-authentic: $(MALICIOUS_AUTHENTIC_TARGETS)

malicious-synthetic: $(MALICIOUS_SYNTHETIC_TARGETS)

%: malicious/authentic/%
	$(MAKE) -C $<

%: malicious/synthetic/%
	$(MAKE) -C $<


clean:
	for authentic_dir in $(MALICIOUS_AUTHENTIC_DIRS); do \
		$(MAKE) -C $$authentic_dir clean; \
	done
	for synthetic_dir in $(MALICIOUS_SYNTHETIC_DIRS); do \
		$(MAKE) -C $$synthetic_dir clean; \
	done


FORCE: ;

.PHONY: all clean FORCE malicious malicious-authentic malicious-synthetic
