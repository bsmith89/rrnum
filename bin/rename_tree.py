#!/usr/bin/env python2

import sys
from Bio import Phylo


def main():
    tree_path = sys.argv[1]
    names_path = sys.argv[2]

    tree = Phylo.read(tree_path, 'newick')
    mapping = make_mapping(names_path)

    for leaf in tree.get_terminals():
        # Because FastTree output is not the same as what Bio.Phylo.read
        # expects.
        leaf.name = mapping[str(leaf.confidence)]
        leaf.confidence = None

    Phylo.write(tree, sys.stdout, 'newick')


def make_mapping(path):
    out = {}
    with open(path) as handle:
        for line in handle:
            key, value = line.split()
            out[key] = value
    return out


if __name__ == "__main__":
    main()
