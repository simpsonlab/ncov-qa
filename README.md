# ncov-qa

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


`ncov-qa` is the workflow used for the quality assessment of COVID-19
data from participating institutes in Ontario.  Each institute provides
results from FAST5/FASTQ files distriubted by [Public Health Ontario](https://www.publichealthontario.ca).


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

To run the pipeline:
```
snakemake -s /path/to/Snakefile --cores num_cores build_snpeff_db
snakemake -s /path/to/Snakefile --cores num_cores all
```

## Credits and Acknowledgements

* The `quick_align.py` script was obtained from [ncov-random-scripts](https://github.com/jts/ncov-random-scripts)


## Authors

* Richard J. de Borja <richard.deborja@oicr.on.ca>

* Jared T. Simpson


## License
`MIT`
