import os
import sys
import vcf
import argparse


def init_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--vcf', required=True,
            help='VCF file to process')
    parser.add_argument('-r', '--refvcf', required=True,
            help='reference VCF use to compare against')
    return parser.parse_args()


def main():
    """
    Main program
    """
    args = init_args()
    vcf_list = list()
    ref_vcf_list = list()
    vcf_reader = vcf.Reader(filename=args.vcf)
    for var in vcf_reader:
        vcf_list.append(var)
    ref_vcf_reader = vcf.Reader(filename=args.refvcf)
    for var in ref_vcf_reader:
        ref_vcf_list.append(var)
    print(ref_vcf_list)


if __name__ == '__main__':
    main()


#__END__
