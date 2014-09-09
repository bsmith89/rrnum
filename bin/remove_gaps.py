#!/usr/bin/env python2

import sys
from Bio import AlignIO, SeqIO
from Bio.Seq import Seq
from numpy import array, ones_like


def main():
    try:
        infile = sys.argv[1]  # AlignIO.read can take a handle or a path
    except IndexError:
        infile = sys.stdin
    alignment = AlignIO.read(infile, 'fasta')
    ncols = alignment.get_alignment_length()
    nseqs = len(alignment)
    empty_cols = []
    sys.stderr.write("Identifying gaps...\n")
    for i in range(ncols):
        if set(alignment[:, i]) == {'-'}:
            empty_cols.append(i)
        sys.stderr.write("\r%f.1%% " %
                         ((100.0 * i) / ncols))
    sys.stderr.write("done.  %d found\n" % len(empty_cols))
    sys.stderr.write("Ungapping sequences: \n")
    for i, rec in enumerate(alignment):
        rec.seq = Seq(remove_items(rec.seq, empty_cols))
        sys.stderr.write("\r%f.1%%" % (100.0 * i / nseqs))
        SeqIO.write(rec, sys.stdout, 'fasta')
    sys.stderr.write("done.\n")


def remove_items(seq, to_remove):
    seq_array = array(list(seq))
    mask = ones_like(seq_array, dtype='?')
    mask[to_remove] = False
    return ''.join(seq_array[mask])

if __name__ == "__main__":
    main()
