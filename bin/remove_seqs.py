#!/usr/bin/env python

import sys
from Bio.SeqIO import parse, write

def main():
    with open(sys.argv[1]) as names_handle:
        remove_names = set(line.strip() for line in names_handle)

    out_recs = []
    for rec in parse(sys.stdin, 'fasta'):
        if rec.name in remove_names:
            continue
        else:
            out_recs.append(rec)

    write(out_recs, sys.stdout, 'fasta')

if __name__ == '__main__':
    main()
