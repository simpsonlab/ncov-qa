
# Helper functions
#
def get_lineage_report(wildcards):
    """
    Return the path to the lineage report 
    """
    lineage = list()
    #lineage_report = f"lineages/{config['institute_id']}_lineage_report.csv"
    lineage.append(f"lineages/{config['institute_id']}_lineage_report.csv")
    lineage.append(f"lineages/{config['institute_id']}_pangolin_version.txt")
    return lineage
    #return lineage_report

def get_consensus_sequences(wildcards):
    """
    Return a list of consensus genome files in FASTA format
    """
    pattern = get_consensus_pattern()
    consensus_sequences = [pattern.format(data_root=config['data_root'], sample=s) for s in get_sample_names()]
    return consensus_sequences


# Rules


rule all_lineage:
    input:
        get_lineage_report

# merge the consensus sequences together into one fasta, applying a
# completeness threshold to avoid including very poor samples
rule make_merged_consensus:
    input:
        get_consensus_sequences
    output:
        "qa_align/{prefix}_consensus.fasta"
    params:
        rename_script = srcdir("../scripts/preprocess_consensus.py")
    shell:
        "python {params.rename_script} {input} > {output}"


# assign lineages to the consensus genomes using pangolin
rule make_lineage_assignments:
    input:
        "qa_align/{prefix}_consensus.fasta"
    output:
        "lineages/{prefix}_lineage_report.csv"
    threads: workflow.cores
    shell:
        "pangolin --outfile {output} {input}"


# write pangolin version information to a file
# this depends on the pangolin output file to
# trigger it to be rebuilt after every pangolin run
rule make_pangolin_version:
    input:
        "lineages/{prefix}_lineage_report.csv"
    output:
        "lineages/{prefix}_pangolin_version.txt"
    shell:
        "pangolin -v > {output}; pangolin -pv >> {output}"


