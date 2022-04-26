# ncov-qa

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


`ncov-qa` is the workflow used for the quality assessment of COVID-19
data from participating institutes in Ontario.  Each institute provides
results from FAST5/FASTQ files distributed by [Public Health Ontario](https://www.publichealthontario.ca).


## Installation
Download the `ncov-qa` package from GitHub.
```
git clone https://github.com/simpsonlab/ncov-qa
cd ncov-qa
```

It is highly recommended to use `conda` to install dependencies and
tools:
```
conda env create -f workflow/envs/environment.yaml
```

Once the dependencies have been installed, activate the conda
environment:
```
conda activate ncov-qa
```


## Usage

The files submitted by each institute include:

* `summary_qc.tsv`

* `consensus.fasta`

* `lineage_report.csv`


These files should reside or be linked in a `data` directory.

A `config.yaml` file is required to run the pipeline.  The file should use the following as a template:
```
institute_id: "<institute_prefix>"
submitter: "Submitter"
data_root: "data"
consensus_pattern: "{data_root}/{sample}.fasta"
reference: "/path/to/reference_genome.fasta"
mode: "vcf"
summary_sample_name: "{sample}"
```

To run the pipeline:
```
snakemake -s /path/to/ncov-qa/workflow/Snakefile --cores num_cores build_snpeff_db
snakemake -s /path/to/ncov-qa/workflow/Snakefile --cores num_cores all
```

### Output
```
.
├── config.yaml
├── data
├── lineages
│   ├── <institute>_lineage_report.csv
│   └── <institute>_pangolin_version.txt
├── qa_align
├── qa_results
│   └── <institute>.mutation.metadata.tsv
├── snpEff_genes.txt
└── snpEff_summary.html
```


### Compare results to a baseline
To create a merged count table:
```
python /path/to/ncov-qa/scripts/merge_qa_results.py --file /path/to/output/qa_results/<institute>.mutation.metadata.tsv --ref_file /path/to/baseline/output/qa_results/<institute>.mutation.metadata.tsv
```

## Credits and Acknowledgements

* The `quick_align.py` script was obtained from [ncov-random-scripts](https://github.com/jts/ncov-random-scripts)


## Authors

* Richard J. de Borja <richard.deborja@oicr.on.ca>

* Jared T. Simpson


## License
`MIT`
