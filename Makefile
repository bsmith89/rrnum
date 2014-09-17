RAW_FN = raw/rrnDBv1_16S_byron_2014-08-29.fasta
RAW_PROBSEQS_FN = raw/rrnDBv1_16S_byron_problem-seqs_2014-09-04.fasta
RAW_META = raw/rrnDBv1_16S_byron_2014-08-29.meta
RAW_PROBSEQS_META = raw/rrnDBv1_16S_byron_problem-seqs_2014-09-04.meta
SILVA_REF_URL = http://www.arb-silva.de/fileadmin/silva_databases/release_119/ARB_files/SSURef_NR99_119_SILVA_14_07_14_opt.arb
READMES = $(subst .md,.html,README.md $(wildcard */README.md))

all: docs

docs: $(READMES)

seq/16S.fn: $(RAW_FN)
	@mkdir -p $(@D)
	cp $< $@

meta/16S.tsv: $(RAW_META)
	@mkdir -p $(@D)
	cat $< \
		| sed '/^#/d' \
		| sed '1s:^.::' \
		> $@

ref/16S_ref.arb:
	@mkdir -p $(@D)
	curl -o $@ $(SILVA_REF_URL)

seq/16S.afn: seq/16S.fn ref/16S_ref.arb
	sina -i $< --intype=FASTA -o $@ --outtype=FASTA --ptdb 16S_ref.arb

res/16S.probseqs.duplicates.tsv: seq/16S.fn $(RAW_PROBSEQS_FN)
	@mkdir -p $(@D)
	cat $^ \
		| grep '^>' \
		| sort \
		| uniq -d \
		| sed 's:>::' \
		> $@

seq/16S.probseqs.fn: res/16S.probseqs.duplicates.tsv $(RAW_PROBSEQS_FN)
	@mkdir -p $(@D)
	cat $(RAW_PROBSEQS_FN) \
		| bin/remove_seqs.py $< \
		> $@

meta/16S.probseqs.tsv: $(RAW_PROBSEQS_META)
	@mkdir -p $(@D)
	cat $< \
		| sed '/^#/d' \
		| cut -f "1 2 3 4 5" \
		> meta/16S.probseqs.tsv

meta/16S.with_probseqs.tsv: meta/16S.tsv meta/16S.probseqs.tsv
	cat $^ > $@

seq/16S.with_probseqs.fn: seq/16S.fn seq/16S.probseqs.fn
	cat $^ > $@

seq/16S.with_probseqs.afn: seq/16S.with_probseqs.fn ref/16S_ref.arb
	sina -i $< --intype=FASTA -o $@ --outttype=FASTA --ptdb 16S_ref.arb

fig/ident_vs_error.png: bin/ident_vs_error.py res/16S.dists.sample.tsv
	@mkdir -p $(@D)
	$^

pandoc_recipe = \
pandoc -f markdown -t html5 -s \
       --highlight-style pygments --mathjax \
       --toc --toc-depth=4 \
       <$< >$@
%/README.html: %/README.md
	$(pandoc_recipe)
README.html: README.md
	$(pandoc_recipe)

clean:
	rm -f ref/*.arb.log $(READMES)

