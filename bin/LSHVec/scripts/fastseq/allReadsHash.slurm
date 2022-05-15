#!/bin/bash
#SBATCH --mail-user=parth.a.datar@vanderbilt.edu
#SBATCH --mail-type=ALL
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem=100G
#SBATCH --time=10:00

python hashSeq.py -i ../../../data/allReads.seq --hash lsh -o ../../../modelling/allReads.hash -k 10
