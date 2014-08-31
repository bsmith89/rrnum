#!/usr/bin/env python2

import sys
from argparse import ArgumentParser
from Bio import SeqIO
from utils import write_multithread, grouper, get_default_argument_parser


_DEFAULT_FMT = "fasta"
_DEFAULT_N = 2


def main():
    description = 'Split a FASTA file into multiple subfiles.'
    parser = ArgumentParser(description=description,
                            parents=[get_default_argument_parser()])
    parser.add_argument('-f', '--in-format',
                        default=_DEFAULT_FMT,
                        help="A biopython file format string.")
    parser.add_argument('-n', '--num-files', type=int,
                        default=_DEFAULT_N,
                        help=("The number of splits. "
                              "DEFAULT=%d") % _DEFAULT_N)
    parser.add_argument('in_path', nargs='?', default=None,
                        help=("The path of the file to be read in. "
                              "If no argument given, reads from STDIN."))
    parser.add_argument('out_pattern', default=None,
                        help=("Output file names format string. "
                              "Must contain one '%%d' for the file number."))
    args = parser.parse_args()

    if args.in_path is None:
        record_parser = SeqIO.parse(sys.stdin, args.in_format)
    else:
        record_parser = SeqIO.parse(args.in_path, args.in_format)

    write_multithread(grouper(record_parser, 100),
                      lambda recs, handle:
                          SeqIO.write(recs, handle, args.in_format),
                      args.out_pattern, n=args.num_files)

if __name__ == "__main__":
    main()
