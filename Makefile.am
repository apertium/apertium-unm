###############################################################################
## Makefile for apertium-unm
###############################################################################

LANG1=unm
BASENAME=apertium-$(LANG1)

TARGETS_COMMON =			\
	$(LANG1).automorf.hfst		\
	$(LANG1).automorf.bin		\
	$(LANG1).automorf.att.gz	\
	$(LANG1).autogen.hfst		\
	$(LANG1).autogen.bin		\
	$(LANG1).autogen.att.gz		\
	$(LANG1).autopgen.bin		\
	$(LANG1).prob                   \
	$(LANG1).rlx.bin

# This include defines goals for install-modes, .deps/.d, autobil.prefixes and .mode files:
@ap_include@

SHELL = /bin/bash -o pipefail

LEXCFLAGS=-v --Werror

###############################################################################
## Unami transducer
###############################################################################

.deps/$(LANG1).twol.hfst: $(BASENAME).$(LANG1).twol .deps/.d
	hfst-twolc $< -o $@

.deps/$(LANG1).RL.lexd: $(BASENAME).$(LANG1).lexd .deps/.d
	cat $< | grep -v 'Dir/LR' > $@

.deps/$(LANG1).LR.lexd: $(BASENAME).$(LANG1).lexd .deps/.d
	cat $< | grep -v 'Dir/RL' > $@

.deps/$(LANG1).RL.lexd.hfst: .deps/$(LANG1).RL.lexd
	lexd $< | hfst-txt2fst -o $@

.deps/$(LANG1).LR.lexd.hfst: .deps/$(LANG1).LR.lexd
	lexd $< | hfst-txt2fst -o $@


.deps/$(LANG1).RL.hfst: .deps/$(LANG1).RL.lexd.hfst .deps/$(LANG1).twol.hfst
	hfst-compose-intersect -1 .deps/$(LANG1).RL.lexd.hfst -2 .deps/$(LANG1).twol.hfst -o $@

.deps/$(LANG1).LR.hfst: .deps/$(LANG1).LR.lexd.hfst .deps/$(LANG1).twol.hfst
	hfst-compose-intersect -1 .deps/$(LANG1).LR.lexd.hfst -2 .deps/$(LANG1).twol.hfst -o $@

$(LANG1).autogen.hfst: .deps/$(LANG1).RL.hfst
	hfst-fst2fst -O $< -o $@

.deps/spellrelax.hfst: $(BASENAME).$(LANG1).spellrelax .deps/.d
	hfst-regexp2fst -S -o $@ $<

$(LANG1).automorf.hfst: .deps/$(LANG1).LR.hfst .deps/spellrelax.hfst
	hfst-compose-intersect -1 $< -2 .deps/spellrelax.hfst | hfst-invert | hfst-minimise | hfst-fst2fst -O -o $@

$(LANG1).autogen.att.gz: $(LANG1).autogen.hfst
	hfst-fst2txt $< | gzip -9 -c -n > $@

$(LANG1).automorf.att.gz: $(LANG1).automorf.hfst
	hfst-fst2txt $< | gzip -9 -c -n > $@

$(LANG1).autogen.bin: $(LANG1).autogen.att.gz .deps/.d
	zcat < $< > .deps/$(LANG1).autogen.att
	lt-comp lr .deps/$(LANG1).autogen.att $@

$(LANG1).automorf.bin: $(LANG1).automorf.att.gz .deps/.d
	zcat < $< > .deps/$(LANG1).automorf.att
	lt-comp lr .deps/$(LANG1).automorf.att $@

$(LANG1).autopgen.bin: $(BASENAME).post-$(LANG1).dix
	lt-comp lr $< $@

###############################################################################
## Debugging transducers (for testvoc)
###############################################################################


debug: .deps/$(LANG1).LR-debug.hfst .deps/$(LANG1).lexd.hfst


.deps/$(LANG1).LR-debug.hfst: $(BASENAME).$(LANG1).lexd .deps/.d
	cat $< | grep -v 'Dir/RL' | grep -v 'Use/Circ' > .deps/$(LANG1).LR-debug.lexd
	lexd .deps/$(LANG1).LR-debug.lexd | hfst-txt2fst -o .deps/$(LANG1).LR-debug.lexd.hfst
	hfst-compose-intersect -1 .deps/$(LANG1).LR-debug.lexd.hfst -2 .deps/$(LANG1).twol.hfst -o $@

.deps/$(LANG1).lexd.hfst: .deps/$(LANG1).RL.lexd.hfst
	hfst-fst2fst -O -i $< -o $@
###############################################################################
## Disambiguation rules
###############################################################################

$(LANG1).rlx.bin: $(BASENAME).$(LANG1).rlx
	cg-comp $< $@

###############################################################################
## Spell checker
###############################################################################

$(LANG1).zhfst: .deps/acceptor.default.hfst .deps/errmodel.default.hfst
	rm -f $@
	zip -j $@ .deps/acceptor.default.hfst .deps/errmodel.default.hfst speller/index.xml

.deps/errmodel.default.hfst: .deps/words.default.hfst .deps/strings.default.hfst
	python dev/editdist.py -v -s -d 1 -e '@0@' -i speller/editdist.default.txt -a .deps/acceptor.default.hfst \
	| hfst-txt2fst  -e '@0@' -o .deps/editdist.default.hfst
	hfst-disjunct .deps/strings.default.hfst .deps/editdist.default.hfst \
	| hfst-minimise | hfst-repeat -f 1 -t 2 -o .deps/editstrings.default.hfst
	hfst-disjunct .deps/words.default.hfst .deps/editstrings.default.hfst \
	| hfst-fst2fst  -f olw -o $@

.deps/words.default.hfst: speller/words.default.txt
	grep -v -e "^#" -e "^$$" $< | hfst-strings2fst  -j -o $@

.deps/strings.default.hfst: speller/strings.default.txt .deps/anystar.hfst
	grep -v -e "^#" -e "^$$" $< | hfst-strings2fst  -j | hfst-concatenate .deps/anystar.hfst - |\
	hfst-concatenate - .deps/anystar.hfst -o $@

.deps/anystar.hfst:
	echo "?*;" | hfst-regexp2fst -S -o $@

.deps/acceptor.default.hfst: $(LANG1).autogen.hfst
	cat $< | hfst-fst2fst -t | hfst-project  --project=lower | hfst-minimise |hfst-fst2fst  -f olw -o $@


###############################################################################
## Unigram tagger
###############################################################################

$(LANG1).prob: corpus/$(LANG1).tagged
	apertium-tagger -s 0 -u 2 $@ $<

###############################################################################
## Distribution
###############################################################################

EXTRA_DIST= \
		$(BASENAME).$(LANG1).lexd	\
		$(BASENAME).$(LANG1).twol	\
		$(BASENAME).$(LANG1).rlx	\
		$(BASENAME).post-$(LANG1).dix	\
		$(LANG1).prob			\
		modes.xml

###############################################################################
## Installation stuff
###############################################################################
#
#   apertium_unm_dir: This is where the compiled binaries go
#   apertium_unm_srcdir: This is where the source files go

apertium_unmdir=$(prefix)/share/apertium/$(BASENAME)/
apertium_unm_srcdir=$(prefix)/share/apertium/$(BASENAME)/

EXTRA_TARGETS=

if HAVE_HFSTOSPELL
EXTRA_TARGETS += $(LANG1).zhfst
endif # HAVE_HFSTOSPELL

apertium_unm_DATA=$(TARGETS_COMMON) $(EXTRA_TARGETS)

pkgconfigdir = $(prefix)/share/pkgconfig
pkgconfig_DATA = $(BASENAME).pc

noinst_DATA=modes/$(LANG1)-morph.mode

install-data-local: install-modes
	$(INSTALL_DATA) $(BASENAME).$(LANG1).lexd $(DESTDIR)$(apertium_unm_srcdir)
	$(INSTALL_DATA) $(BASENAME).$(LANG1).twol $(DESTDIR)$(apertium_unm_srcdir)
	$(INSTALL_DATA) $(BASENAME).$(LANG1).rlx $(DESTDIR)$(apertium_unm_srcdir)
	$(INSTALL_DATA) $(BASENAME).post-$(LANG1).dix $(DESTDIR)$(apertium_unm_srcdir)

###############################################################################
## Cleanup
###############################################################################

CLEANFILES = $(TARGETS_COMMON)
clean-local:
	-rm -rf .deps modes

###############################################################################
## Test
###############################################################################

test: all
	echo "TODO test sentence" | apertium -d . -f line unm-morph | tee .test-mt
	@echo "TODO test analysis results" > .test-ref
	@diff .test-ref .test-mt
	@rm .test-ref .test-mt
