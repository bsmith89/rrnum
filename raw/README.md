## Source ##
Steve Stoddard made these files for me from rrnDB.

## Files ##
### Sequence ###
#### Path: ####

    ./rrnDBv1_16S_byron_2014-08-29.fasta

#### Format: ####

    >{ID}
    {sequence}
    ...

#### SQL query: ####

```sql
Database=rrndb3;
SELECT s.fid, s.seq
from sequence s
where length(s.seq) >= 1170 and
        length(s.seq) <= 1700
order by s.genomeid, s.fid
```

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

```sql
Database=rrndb3;
SELECT s.fid, s.genomeid, tn.taxid, g.sum16s, tn.name
from sequence s, genome g, taxname tn
where length(s.seq) >= 1170 and
        length(s.seq) <= 1700 and
        s.genomeid=g.genomeid and
        g.taxnameid=tn.taxnameid
order by s.genomeid, s.fid
```

#### Description: ####
Tab separated values of the metadata associated with each FID.
This file allows me to map rrn copy numbers (associated with each genome)
to each sequence.

### Problem Sequences and Metadata ###
#### Paths: ####

    ./rrnDBv1_16S_byron_problem-seqs_2014-09-04.*

#### Format: ####
Same as above except `rrnDBv1_16S_byron_2014-09-04.metadata` has an
additional column and a different query.
Its headers are:

    #fid	genomeid	taxid	rrncopy	orgname	length(s.seq)

#### SQL queries: ####

```sql
Database=rrndb3;
SELECT s.fid, s.genomeid, tn.taxid, g.sum16s, tn.name, length(s.seq)
FROM sequence s, genome g, taxname tn
WHERE s.genomeid IN (336, 591, 1106, 1508, 2330, 2476, 1907, 2212) AND
      s.genomeid=g.genomeid AND
      g.taxnameid=tn.taxnameid
ORDER BY s.genomeid, s.fid
```

#### Description ####
These sequences represent those which did _not_ pass the size filter
used by Steve, but that come from genomes in which other sequences did pass
the size filter.
As of now, these sequences are included in the rrnDB, despite failing the size
cutoff.
Steve S. has asked me to add them to my analysis in order to determine
what's going on.
