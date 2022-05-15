# DipPAV

DipPAV is a long-reads based, haplotyp-specific structural variant detection tool. It employs the power of natural language processing to further haplotype reads that do not cover any heterozygous SNPs, generates high-quality haplotype resolved contigs, and compare contigs against reference to accurately extract structural variants.



### Installation

1. clone the github repository to your local machine
git clone

2. enter the donwloaded folder
cd DipPAV

4. create 2 conda environment

###### DippAV env########
conda create -n "DipPAV" python=3.9.12
conda activate DipPAV
conda install minimap2 samtools jellyfish fasttext svim-asm truvari multicore-tsne longshot numpy scikit-learn joblib tqdm pandas cython xlwt
conda deactivate
###### LSHvec env########
conda create -n "LSHvec" python=3.7
conda activate LSHvec
conda install minimap2 fasttext svim-asm truvari multicore-tsne longshot numpy scikit-learn joblib tqdm pandas cython
pip install bin/LSHvec/pysparc-0.1-cp37-cp37m-linux_x86_64.whl
conda deactivate

You are all set.

### Run DipPAV

#### Input data

You need to provide a reference file ### DippAV env########
conda create -n "DipPAV" python=3.9.12
conda activate DipPAV
conda install minimap2 samtools jellyfish fasttext svim-asm truvari multicore-tsne longshot numpy scikit-learn joblib tqdm pandas cython xlwt
conda deactivate
### LSHvec env########
conda create -n "LSHvec" python=3.7
conda activate LSHvec
conda install minimap2 fasttext svim-asm truvari multicore-tsne longshot numpy scikit-learn joblib tqdm pandas cython
pip install bin/LSHvec/pysparc-0.1-cp37-cp37m-linux_x86_64.whl
conda deactivate


