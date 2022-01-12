#!/usr/bin/env python

import os
import sys
import argparse
import vcf


def init_args():
    """
    Initialize command line arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', required=True,
            help='path to the VCF file to process')
    parser.add_argument('-o', '--out', required=True,
            help='filename to write filtered VCF to')
    return parser.parse_args()


def is_n(var):
    """
    Determine if the variant is N
    """
    if list(set(list(str(var.ALT[0]))))[0] == 'N':
        return True
    else:
        return False


def replace_del_alt(var):
    """
    Issues occur with deletions hear the ends of the genome.
    Currently - is used to represent an entire string of bases
    being deleted.  Here we replace the ALT with "N" the length
    of REF.
    """
    ref_length = len(var.REF)    
    if var.ALT[0] == '-':
        fixed_alt = 'N' * ref_length
        var.ALT[0] = fixed_alt
        return var
    else:
        return var


def is_mnp(var):
    """
    Determine if the variant is a multi-nucleotide polymorphism
    """
    ref_length = len(var.REF)
    var_length = len(var.ALT[0])
    if ref_length > 0:
        if (ref_length == var_length):
            pass
        else:
            return var
    else:
        return var


def main():
    """
    Main function
    """
    args = init_args()
    vcf_reader = vcf.Reader(filename=args.file)
    with open(args.out, 'w') as ofh:
        vcf_writer = vcf.Writer(ofh, vcf_reader)
        for var in vcf_reader:
            if is_n(var):
                continue
            elif var.is_deletion:
                fixed_var = replace_del_alt(var=var)
                vcf_writer.write_record(fixed_var)
            else:
                vcf_writer.write_record(var)



if __name__ == '__main__':
    main()


#__END__
