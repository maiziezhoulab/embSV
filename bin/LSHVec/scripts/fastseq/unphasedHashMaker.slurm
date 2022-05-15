#!/bin/bash
#SBATCH --mail-user=parth.a.datar@vanderbilt.edu
#SBATCH --mail-type=ALL
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem=60G
#SBATCH --time=10:00

python hashSeq.py -i ../../../data/unphased_reads/PS94_96.seq --hash lsh -o ../../../modelling/PS94_96.hash -k 20
