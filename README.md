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
