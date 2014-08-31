This is an analysis of the amount of copy number information available to us
from 16S sequence.

Basically, I'm going to try to asses how well our database informs us of
the copy number of a random sequence.


#### 2014-08-29 ####
I received `rrnDBv1_16S_byron_2014-08-29.fasta` and
`rrnDBv1_16S_byron_2014-08-29.meta` from Steve Stoddard.

    cat seq/16S.fn | grep '^>' | sort | uniq -d
    # Returns Nothing
    cat seq/16S.fn | grep '^>' -c
    # Returns '10056'
    # Their are this many sequences.

On the MSU HPCC (because
(`sina`)[http://www.arb-silva.de/aligner/sina-download/] doesn't run on OSX),
I downloaded `sina` and the aligned reference NR.

    mkdir scratch; cd scratch
    curl -O http://www.arb-silva.de/fileadmin/silva_databases/SINA/1.2.11/sina-1.2.11_centos5_amd64.tgz
    # Downloads 3.417k
    tar -xzf sina-1.2.11_cenos5_amd64.tgz
    ln -s sina-1.2.11/sina sina
    curl -O http://www.arb-silva.de/fileadmin/silva_databases/release_119/Exports/SILVA_119_SSURef_Nr99_tax_silva_full_align_trunc.fasta.gz
    # Downloads 1061M
    gunzip SILVA_119_SSURef_Nr99_tax_silva_full_align_trunc.fasta.gz
    # Takes a little while to run.  It's 26GB...!
    # I don't even think I can run this next command:
    cat SILVA_119_SSURef_Nr99_tax_silva_full_align_trunc.fasta | grep '^>' -c
    # Yep, it's taking forever.
    # Output: 534968  Finally.  Half a million sequences!
    sina -i SILVA_119_SSURef_Nr99_tax_silva_full_align_trunc.fasta -o 16S_ref.arb

This was going to take numerous hours to run.  Turns out there's a much
simpler way.

    curl -o 16S_ref.arb http://www.arb-silva.de/fileadmin/silva_databases/release_119/ARB_files/SSURef_NR99_119_SILVA_14_07_14_opt.arb
    # This is the pre-built ARB database for sina
    # Now I can align with just:
    sina -i 16S.fn --intype=FASTA -o 16S.afn --outtype=FASTA --ptdb 16S_ref.arb

Alignment is now the time limiting step.
Instead of parallelizing myself, I'm going to use the ad-hoc parallelization
built in to `sina`.

    # Reformat the sequences as ARB
    sina -i 16S.afn --intype=FASTA -o 16S.arb --prealigned
    # Do an offset/skip run on the ARB file.
    for i in $(seq 1 10); do
        sina -i 16S.arb -o 16S.f$i.afn --ptdb 16S_ref.arb
        --select-step=10 --select-skip=$i
    # This takes more like 20 minutes, and I just have to concatenate my
    # output files in the end.


#### 2014-08-30 ####
I finally got my sequence splitter working.
I split up all of the rrnDB sequences into 16 files,

    bin/split_seqs.py -n 16 seq/16S.fn seq/splits/16S.split%02d.fn

`scp`ed them to MSU's hpcc and ran `sina` on all of them.

    for file in 16S.split*.fn; do
        sina -i $file --intype=FASTA -o ${file/.fn/.afn} --outtype=FASTA \
             --ptdb 16S_ref.arb
    cat 16S.split*.afn > 16S.afn

This took less than an hour, if I remember correctly.

I then concatenated the resulting alignments, and ran FastTree

    fasttree -nt 16S.afn > 16S.afn.tre

locally (OSX) to estimate a phylogeny.  This took approximately
9 hours.  I think it would have been much faster if I had ungapped the
alignment first.
I'm not sure if this will actually do anything for the full alignment,
because *some* organism's sequence must be filling those positions, and I'm
using the full RefSeq database through KEGG.


#### 2014-08-31 ####
I'm going to try and rename the ID's in 16S.afn.tre to something that's
easier to interpret.

    cat 16S.tsv | awk '{print $1 "\t" $2 "_" $1}' > 16S.id_map.tsv

I've written `bin/rename_tree.py` to import the tree (`Bio.Phylo`),
rename each leaf, and then export the tree.
But now I'm finding that `Bio.Phylo` doesn't read the output of FastTree
correctly; leaf names are read as 'confidence' fields.

I'm not sure if the problem lies with FastTree, `Bio.Phylo`, or me.
While I can fix it, I don't like the idea of `bin/rename_tree.py` assuming
that newick trees are in a different format than `Bio.Phylo` does.

    bin/rename_tree.py seq/16S.afn.tre meta/16S.id_map.tsv \
        > seq/16S.afn.rename.tre

I then explored this phylogeny in an ipython notebook
(`tree_exploration.ipynb`) and output some data.
Specifically, `tre/distances.txt` is a file with one row per genomeid.
Each row is composed of the genomeid, a tab, and then a comma separated list of
all of the pairwise distances between the sequences which were placed on that
tree from that genome.

From 10056 sequences on the tree, there were 2602 unique genomeids, and
1260 genomes had 16S features with divergent sequences.
Of these, the average distance was 0.033, and the mean per-genome maximum
distance was 0.032.
The fact that the latter is smaller is strong evidence that large distances
tend to be found under the same genomeid (which makes sense, since we're
talking about 'all pairwise distances').


