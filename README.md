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
