#!/usr/bin/env python


import csv
import sys
import os
import argparse


def init_args():
    """
    Initialize command line arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', required=True,
            help='QA results file to process')
    parser.add_argument('-r', '--ref_file', required=True,
            help='QA results file from reference genome')
    return parser.parse_args()





def main():
    """
    Main program
    """
    args = init_args()
    d1 = dict()
    d2 = dict()
    with open(args.file, 'r') as fh1:
        d1_reader = csv.DictReader(fh1, delimiter='\t')
        for line in d1_reader:
            d1.update({line['sample'] : line})
    fh1.close()
    with open(args.ref_file, 'r') as fh2:
        reader = csv.DictReader(fh2, delimiter='\t')
        for line in reader:
            d2.update({line['sample'] : line})
    fh2.close()
    print('\t'.join(['sample', 'total_n', 'total_snp', 'total_insertion', 'total_deletion', 'total_frameshift', 'completeness']))
    for sample in d1:
        if sample in d2:
            print(sample + '\t' +
                  d1[sample]['total_n'] + ' (' + d2[sample]['total_n'] + ')\t' +
                  d1[sample]['total_snp'] + ' (' + d2[sample]['total_snp'] + ')\t' +
                  d1[sample]['total_insertion'] + ' (' + d2[sample]['total_insertion'] + ')\t' +
                  d1[sample]['total_deletion'] + ' (' + d2[sample]['total_deletion'] + ')\t' +
                  d1[sample]['total_frameshift'] + ' (' + d2[sample]['total_frameshift'] + ')\t' +
                  d1[sample]['completeness'] + ' (' + d2[sample]['completeness'] + ')')



if __name__ == '__main__':
    main()


#__END__
