import os
import sys
import argparse
import csv


def init_args():
    """
    Initialize command line arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', required=True,
            help='summary_qc.tsv file to review')
    parser.add_argument('-r', '--refsummary', required=True,
            help='reference summary_qc.tsv file to compare')
    parser.add_argument('-d', '--delimiter', default='_',
            help='sample name delimiter in the sample column')
    return parser.parse_args()


def create_entry(line):
    """
    Create a new dictionary entry
    """
    entry = dict()
    # clean up the sample name as some have white space
    sample = line['sample'].strip()
    entry[sample] = {
            'num_consensus_snvs': line['num_consensus_snvs'],
            'num_consensus_n': line['num_consensus_n'],
            'mean_sequencing_depth': line['mean_sequencing_depth'],
            'genome_completeness': line['genome_completeness'],
            'lineage': line['lineage']}
    return entry


def import_summary_tsv_data(file):
    """
    Import the data from a summary_qc.tsv file
    """
    _qc = dict()
    with open(file, 'r') as ifh:
        reader = csv.DictReader(ifh, delimiter='\t')
        for item in reader:
            if item['sample'] not in _qc:
                _qc.update(create_entry(line=item))
            else:
                print(f"Sample: {item['sample']} already processed")
                sys.exit(1)
    return _qc


def get_sample_name(sample, delimiter='_', index=0):
    """
    Return the sample name
    """
    return sample.split(delimiter)[index]


def main():
    """
    Main program
    """
    qc = dict()
    args = init_args()
    samples = list()
    qc = import_summary_tsv_data(file=args.file)
    qc_ref = import_summary_tsv_data(file=args.refsummary)
    print(qc_ref)
    for entry in qc_ref:
        samples.append(entry)
    print('\t'.join(['sample', 'num_consensus_snvs', 'ref_num_consensus_snvs',
        'num_consensus_n', 'ref_num_consensus_n', 'genome_completeness', 'ref_genome_completeness']))
    for sample in samples:
        sample = sample.strip()
        if qc[sample] and qc_ref[sample]:
            print('\t'.join([
                sample,
                qc[sample]['num_consensus_snvs'],
                qc_ref[sample]['num_consensus_snvs'],
                qc[sample]['num_consensus_n'],
                qc_ref[sample]['num_consensus_n'],
                qc[sample]['genome_completeness'],
                qc_ref[sample]['genome_completeness']
                ]))
        else:
            continue


if __name__ == '__main__':
    main()


#__END__
