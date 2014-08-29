## Source ##
Steve Stoddard made these two files for me from rrnDB.

## Files ##
### Sequence ###
#### Path: ####

    ./rrnDBv1_16S_byron_2014-08-29.fasta

#### Format: ####

    >{ID}
    {sequence}
    ...

#### SQL query: ####

    Database=rrndb3;
    SELECT s.fid, s.seq
    from sequence s
    where length(s.seq) >= 1170 and
          length(s.seq) <= 1700
    order by s.genomeid, s.fid

#### Description: ####
Nucleotide FASTA file of rrn genes from the rrnDB, labeled by their FID
(feature ID).

### Metadata ###
#### Path: ####

    ./rrnDBv1_16S_byron_2014-08-29.meta

#### Format: ####

    #{SQL query *.meta}
    #{SQL query *.fasta}
    #
    #fid	genomeid	taxid	rrncopy	orgname
    {entries}
    ...

#### SQL query: ####

    Database=rrndb3;
    SELECT s.fid, s.genomeid, tn.taxid, g.sum16s, tn.name
    from sequence s, genome g, taxname tn
    where length(s.seq) >= 1170 and
          length(s.seq) <= 1700 and
          s.genomeid=g.genomeid and
          g.taxnameid=tn.taxnameid
    order by s.genomeid, s.fid

#### Description: ####
Tab separated values of the metadata associated with each FID.
This file allows me to map rrn copy numbers (associated with each genome)
to each sequence.
