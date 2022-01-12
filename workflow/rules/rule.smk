#
# A child snakemake file that can be included in the main
# Snakefile
#

import glob

configfile: "config.yaml"

def get_institute_id():
    return config.get("institute_id", "default")


def get_consensus_pattern():
    """
    Return the consensus_pattern value in the config YAML
    file otherwise return a default pattern.
    """
    return config.get("consensus_pattern", "{data_root}/{sample}.consensus.fasta")


def get_sample_names():
    """
    Return a list of sample names obtained from the consensus
    FASTA files
    """
    # get all consensus FASTA genomes in the directory
    # based on the pattern
    pattern = get_consensus_pattern()
   
    # form a glob we can use to get the FASTA files for
    # each sample
    gs = pattern.format(data_root=config["data_root"], sample="*")
    
    genomes = glob.glob(gs)
    samples = set()
    for g in genomes:
        f = os.path.basename(g)
        fields = f.split(".")
        samples.add(fields[0])

    return list(samples)


def get_consensus_file(wildcards):
    """
    Get the consensus FASTA file from the 'data_root' directory
    """
    data_root = config['data_root']
    pattern = get_consensus_pattern()
    out = pattern.format(data_root=config['data_root'], sample=wildcards.sample)
    return out


def get_align_vcf_files(wildcards):
    """
    Return a list of VCF files from the quick_align.py output
    """
    pattern = "qa_align/{sample}.align.vcf"
    align_vcf_files = [pattern.format(sample=s) for s in get_sample_names()]
    return align_vcf_files


def get_annotated_vcf_files(wildcards):
    """
    Return a list of annotated VCF files from SNPEff
    """
    pattern = "qa_align/{sample}.ann.vcf"
    annotated_vcf_files = [pattern.format(sample=s) for s in get_sample_names()]
    return annotated_vcf_files


def get_mutation_metadata_files(wildcards):
    """
    Return a list of mutation metadata files generated from
    count_mutations.py
    """
    pattern = "qa_align/{sample}.mutation.metadata.tsv"
    mutation_metadata_files = [pattern.format(sample=s) for s in get_sample_names()]
    return mutation_metadata_files


def get_merged_mutation_metadata_file(wildcards):
    """
    Return the final merged mutation metadata file
    """
    institute_id=get_institute_id()
    return f"qa_results/{institute_id}.mutation.metadata.tsv"


def get_lineage_reports(wildcards):
    """
    Return the full path to the lineage report and the pangolin version
    file
    """
    out = list()
    out.append(f'lineages/{get_institute_id()}_pangolin_version.txt')
    return out

#
# Top-level rule
#
rule all_align:
    input:
        expand("qa_align/{s}.ann.vcf", s=get_sample_names())

    
rule get_align_vcf:
    input:
        reference=config['reference'],
        genome=get_consensus_file
    output:
        "qa_align/{sample}.align.vcf"
    params:
        script=srcdir("../scripts/quick_align.py"),
        mode="vcf"
    shell:
        "python {params.script} --genome {input.genome} --reference-genome {input.reference} --output-mode {params.mode} > {output}"


rule filter_vcf:
    input:
        "qa_align/{sample}.align.vcf"
    output:
        "qa_align/{sample}.align.filter.vcf"
    params:
        script=srcdir("../scripts/filter_vcf.py")
    shell:
        "python {params.script} --file {input} --out {output}"


rule run_snpeff:
    input:
        "qa_align/{sample}.align.filter.vcf"
    output:
        "qa_align/{sample}.ann.vcf"
    params:
        script="snpEff",
        db="MN908947.3",
        aa_letter="-hgvs1LetterAa",
        no_log="-noLog"
    shell:
        "{params.script} {params.no_log} {params.aa_letter} {params.db} {input} > {output}"

rule count_mutations:
    input:
        vcf="qa_align/{sample}.ann.vcf",
        fasta=get_consensus_file
        #fasta="data/{sample}.consensus.fasta"
    output:
        "qa_align/{sample}.mutation.metadata.tsv"
    params:
        script=srcdir("../scripts/count_mutations.py")
    shell:
        "python {params.script} --vcf {input.vcf} \
                                --fasta {input.fasta} \
                                --sample {wildcards.sample} > {output}"

rule merge_mutations_count:
    input: expand("qa_align/{s}.mutation.metadata.tsv", s=get_sample_names())
    output: "qa_results/{prefix}.mutation.metadata.tsv"
    params:
        path="qa_align",
        script=srcdir("../scripts/merge_results.py")
    shell:
        "python {params.script} --path {params.path} > {output}"

