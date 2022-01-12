#!/usr/bin/env python


import os
import sys
import argparse
import csv

def init_args():
    """
    Initialize command line arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', required=True,
            help='path to search mutation metadata files')
    parser.add_argument('--pattern', default='.mutation.metadata.tsv',
            help='filename pattern (default: .mutation.metadata.tsv)')
    return parser.parse_args()


def print_header():
    """
    Print the mutation metadata header line.
    """
    header = ['sample',
              'total_n',
              'total_snp',
              'total_insertion',
              'total_deletion',
              'total_frameshift',
              'completeness']
    print('\t'.join(header))


def print_line(sample, line):
    """
    Print the line as tab separated
    """
    genome_completeness = round(float(line['completeness']), ndigits=4)
    print('\t'.join([sample,
                     line['total_n'],
                     line['total_snp'],
                     line['total_insertion'],
                     line['total_deletion'],
                     line['total_frameshift'],
                     str(genome_completeness)]))


def create_dict_entry(line):
    """
    Construct a dictionary entry using the sample as the key
    """
    sample_dict = {line['sample'] : {
        'total_n': line['total_n'],
        'total_snp': line['total_snp'],
        'total_insertion': line['total_insertion'],
        'total_deletion': line['total_deletion'],
        'total_frameshift': line['total_frameshift'],
        'completeness': line['completeness']
        }}
    return sample_dict


def main():
    """
    Main program
    """
    args = init_args()
    print_header()
    results_dict = dict()
    sample_names = list()
    for root, dirs, files in os.walk(args.path):
        for file in files:
            if file.endswith(args.pattern):
                with open('/'.join([root, file]), 'r') as ifh:
                    item = csv.DictReader(ifh, delimiter='\t')
                    for row in item:
                        #print_line(row)
                        results_dict.update(create_dict_entry(line=row))
                        sample_names.append(row['sample'])
                ifh.close()
    sample_names.sort()
    for sample in sample_names:
        print_line(sample=sample, line=results_dict[sample])
        
        


if __name__ == '__main__':
    main()


#__END__
