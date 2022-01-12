#!/usr/bin/env python


import collections
import pysam
import os
import sys
import re
import argparse


def init_args():
    """
    Process command line argument
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file',
            help='full path to FASTA file to process')
    return parser.parse_args()


def count_n(file):
    """
    Count the number of Ns in a consensus sequence
    """
    fa = pysam.FastxFile(file)
    for record in fa:
        base_counter = collections.Counter()
        for base in record.sequence:
            base_counter.update(base.upper())
    return base_counter['N']
    

def main():
    """
    Main program to be executed
    """
    args = init_args()
    total_n = count_n(file=args.file)
    print(f"total N: {total_n}")


if __name__ == '__main__':
    main()


#__END__
