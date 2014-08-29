seq/16S.fn: raw/rrnDBv1_16S_byron_2014-08-29.fasta
	mkdir $(@D)
	cp $< $@

meta/16S.tsv: raw/rrnDBv1_16S_byron_2014-08-29.meta
	mkdir $(@D)
	cat $< | sed '1,3d' | sed '1s:^.::' > $@
