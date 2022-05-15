#!/bin/bash
#SBATCH --mail-user=parth.a.datar@vanderbilt.edu
#SBATCH --mail-type=ALL
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem=30G
#SBATCH --time=30:00

python hashSeq.py -i ../../../data/phased_reads/PS94_hp1.seq --hash lsh -o ../../../modelling/PS94_hp1.hash -k 20
python hashSeq.py -i ../../../data/phased_reads/PS94_hp2.seq --hash lsh -o ../../../modelling/PS94_hp2.hash -k 20
python hashSeq.py -i ../../../data/phased_reads/PS96_hp1.seq --hash lsh -o ../../../modelling/PS96_hp1.hash -k 20
python hashSeq.py -i ../../../data/phased_reads/PS96_hp2.seq --hash lsh -o ../../../modelling/PS96_hp2.hash -k 20
python hashSeq.py -i ../../../data/unphased_reads/PS94_96.seq --hash lsh -o ../../../modelling/PS94_96.hash -k 20
