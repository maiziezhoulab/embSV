#!/bin/bash
#SBATCH --mail-user=parth.a.datar@vanderbilt.edu
#SBATCH --mail-type=ALL
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem=60G
#SBATCH --time=10:00

./lshvec skipgram -input ../modelling/PS94_96.hash -output ../results/PS94_96_lsh -minCount 1
