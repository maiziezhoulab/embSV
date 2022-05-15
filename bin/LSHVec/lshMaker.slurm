#!/bin/bash
#SBATCH --mail-user=parth.a.datar@vanderbilt.edu
#SBATCH --mail-type=ALL
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem=30G
#SBATCH --time=30:00

./lshvec skipgram -input ../modelling/PS94_hp1.hash -output ../results/PS94_hp1_lsh -minCount 1
./lshvec skipgram -input ../modelling/PS94_hp2.hash -output ../results/PS94_hp2_lsh -minCount 1
./lshvec skipgram -input ../modelling/PS96_hp1.hash -output ../results/PS96_hp1_lsh -minCount 1
./lshvec skipgram -input ../modelling/PS96_hp2.hash -output ../results/PS96_hp2_lsh -minCount 1
./lshvec skipgram -input ../modelling/PS94_96.hash -output ../results/PS94_96_lsh -minCount 1
