#!/bin/bash
#SBATCH --mail-user=parth.a.datar@vanderbilt.edu
#SBATCH --mail-type=ALL
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem=30G
#SBATCH --time=10:00

python fastqToSeq.py -i ../../../data/unphased_reads/PS9475452_9595386_PS9645569_9739958.fastq -o ../../../data/unphased_reads/PS94_96.seq
