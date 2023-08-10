# Infant Vaccine Response Cohort Data and Code Repository

This repo contains all data, scripts and notebooks to generate all data, statistics and figures for the infant vaccine response cohort.

## Running the code in this repository

### Setting up dependencies in a conda environment

In the top of folder of this repository is a file called `environment.yml`. To build a conda environment with all dependencies necessary to run all scripts and notebooks build a conda environment using that file using this command: `conda env create --file environment.yml -n imc_v2`.

### Matching the data from the manuscript/running fresh

Some steps involved in generating the data for this manuscript include some level of randomness. Therefore results may not be exactly the same if you rerun a script which generates a data file used in the anaylsis. The data files used here are the exact ones which were used in the manuscript so if you want to exactly replicate those results then you should not rerun scripts which will regenerate the data used in those plots/statistical analyses.

Scripts which are known to include randomness and therefore not be perfectly replicated include:
- generate_filtered_and_rarefied_nasal_16S.r
- otu_beta_diversity.ipynb
- kraken_beta_diversity.ipynb
- ko_beta_diversity.ipynb

## Data files

Information about the data files can be found in the READMEs in the relevant folders.

