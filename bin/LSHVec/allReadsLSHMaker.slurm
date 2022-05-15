#!/bin/bash
#SBATCH --mail-user=parth.a.datar@vanderbilt.edu
#SBATCH --mail-type=ALL
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem=60G
#SBATCH --time=20:00

./lshvec skipgram -input ../modelling/allReads.hash -output ../results/allReadsLSH -minCount 1
