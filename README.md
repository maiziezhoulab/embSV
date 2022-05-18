# DipPAV

DipPAV is a long-reads based, haplotype-resolved assembly-based structural variant detection tool. It employs the power of natural language processing to assist partitioning reads for halotype-specific assembly.



## Installation

1. clone the github repository to your local machine
 
```
git clone https://github.com/maiziezhoulab/DipPAV.git
```

2. enter the donwloaded folder
```
cd DipPAV
```

4. create 2 conda environment

```
conda create -n "DipPAV" python=3.9.12
conda activate DipPAV
conda install minimap2 samtools jellyfish fasttext svim-asm truvari multicore-tsne longshot numpy scikit-learn joblib tqdm pandas cython xlwt
conda deactivate

conda create -n "LSHvec" python=3.7
conda activate LSHvec
conda install minimap2 fasttext svim-asm truvari multicore-tsne longshot numpy scikit-learn joblib tqdm pandas cython
pip install bin/LSHvec/pysparc-0.1-cp37-cp37m-linux_x86_64.whl
conda deactivate
```
You are all set.

## Run DipPAV

### Input data

You need to provide a reference fasta file, a chormosome-specific BAM file along with its index file (recommended aligner: NGMLR).

### Step 1

```
conda activate DipPAV
python3 DipPAV_step1.py \
--input_bam ./NA24385_aligned_by_ngmlr_chr21.bam \
--file_prefix NA24385_aligned_by_ngmlr_chr21 \
--chr_num 21 \
--output_dir DipPAV_chr21_result/ \
--ref_genome ./refdata-hg19-2.1.0/fasta/genome.fa
conda deactivate
```

#### *Required parameters
**--input_bam:** "NA24385_aligned_by_ngmlr_chr21.bam" is a bam file generated from long reads aligned by aligner like NGMLR. How to get the bam file, you can also check <a href="xxxxxxxx">here</a>.

**--file_prefix:** file name prefix used to create intermediate file name. You can set it according to your preference.

**--chr_num:** chromosome number (1-22). 

**--output_dir:** output folder. Specify output folder to store the intermidiate and file result(should keep same folder from step1-3).

**--ref_genome:** "./refdata-hg19-2.1.0/fasta/genome.fa" is the reference genome file that the long reads file is aligned to. How to get the fasta file, you can also check <a href="xxxxxxxx">here</a>.

### Step 2

```
conda activate LSHvec
python3 DipPAV_step2.py \
--file_prefix NA24385_aligned_by_ngmlr_chr21 \
--output_dir DipPAV_chr21_result/ \
--num_bucket 20000000 \
--kmer_size 15 \
--dim 200 
conda deactivate
```
#### *Required parameters
**--file_prefix:** file name prefix used to create intermediate file name. You can set it according to your preference.

**--output_dir:** output folder. Specify output folder to store the intermidiate and file result(should keep same folder from step1-3).

#### *Optional parameters

**--num_bucket:** number of bucket to store the kmers in LSH step (5000-20000000). Default = 20000000.

**--kmer_size:** size of kmer used for kmer embedding (10-45). Default = 15.

**--dim:** dimension of features to represent kmers (50-400). Default = 200.


### Step 3

```
conda activate DippAV
python3 DipPAV_step3.py \
--chr_num 21 \
--output_dir DipPAV_chr21_result/ \
--ref_genome ./refdata-hg19-2.1.0/fasta/genome.fa
conda deactivate
```
#### *Required parameters
**--chr_num:** chromosome number (1-22). 

**--output_dir:** output folder. Specify output folder to store the intermidiate and file result(should keep same folder from step1-3).

**--ref_genome:** "./refdata-hg19-2.1.0/fasta/genome.fa" is the reference genome file that the long reads file is aligned to. How to get the fasta file, you can also check <a href="xxxxxxxx">here</a>.


## Final Output:

When all steps finish running, you can go to the output folder you specified in "input.config". Under the output folder, you can see phasing_result, word_embedding_result, clustering_result and assembly_result. The contigs file is under "assembly_result/final_contigs/", and the variants file is "assembly_result/final_contigs/variant_call/DipPAV_variants.vcf".




