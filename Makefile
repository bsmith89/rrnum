RAW_FN = raw/rrnDBv1_16S_byron_2014-08-29.fasta
RAW_META = raw/rrnDBv1_16S_byron_2014-08-29.meta
SILVA_REF_URL = http://www.arb-silva.de/fileadmin/silva_databases/release_119/ARB_files/SSURef_NR99_119_SILVA_14_07_14_opt.arb
SINA_PROCS = 8

seq/16S.fn: $(RAW_FN)
	@mkdir -p $(@D)
	cp $< $@

meta/16S.tsv: $(RAW_META)
	@mkdir -p $(@D)
	cat $< | sed '1,3d' | sed '1s:^.::' > $@

ref/16S_ref.arb:
	@mkdir -p $(@D)
	curl -o $@ $(SILVA_REF_URL)

#seq/16S.afn: seq/16S.fn ref/16S_ref.arb
#	@mkdir -p $(@D)
#	sina -i $< --intype=FASTA -o $@ --outtype=FASTA --ptdb 16S_ref.arb

seq/16S.arb: seq/16S.fn
	@mkdir -p $(@D)
	sina -i $< --intype=FASTA -o $@ --prealigned

## This doesn't appear to work.
#seq/16S.afn: seq/16S.arb ref/16S_ref.arb
#	@mkdir -p $(@D)
#	for i in $(seq 1 $(SINA_PROCS)); do; \
#		sina -i $< --intype=ARB -o $@.temp$i.afn --outtype=FASTA --ptdb 16S_ref.arb \
#		     --select-step $(SINA_PROCS) --select-skip $i
#	cat $@.temp*.afn > $@
#	rm $@.temp*.afn

pandoc_recipe = \
pandoc -f markdown_github -t html5 -s \
       --highlight-style pygments --mathjax \
       --toc --toc-depth=4 \
       <$< >$@
%/README.html: %/README.md
	$(pandoc_recipe)
README.html: README.md
	$(pandoc_recipe)

clean:
	rm -f ref/*.arb.log */README.html

