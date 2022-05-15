# DipPAV

DipPAV is a long-reads based, haplotyp-specific structural variant detection tool. It employs the power of natural language processing to further haplotype reads that do not cover any heterozygous SNPs, generates high-quality haplotype resolved contigs, and compare contigs against reference to accurately extract structural variants.



## Installation

1. clone the github repository to your local machine
git clone

2. enter the donwloaded folder
cd DipPAV

4. create 2 conda environment


conda create -n "DipPAV" python=3.9.12
conda activate DipPAV
conda install minimap2 samtools jellyfish fasttext svim-asm truvari multicore-tsne longshot numpy scikit-learn joblib tqdm pandas cython xlwt
conda deactivate

conda create -n "LSHvec" python=3.7
conda activate LSHvec
conda install minimap2 fasttext svim-asm truvari multicore-tsne longshot numpy scikit-learn joblib tqdm pandas cython
pip install bin/LSHvec/pysparc-0.1-cp37-cp37m-linux_x86_64.whl
conda deactivate

You are all set.

## Run DipPAV

### Input data

You need to provide a reference fasta file, a chormosome-specific BAM file along with its index file.

### Edit input.config

After you clone the github repository, you can see the input.config in the first level of DipPAV folder. You need to edit it, providing the BAM file path, file prefix, reference path, chromosome number etc.

Here is an example of how you can edit this file.

<details><summary>Input.config example</summary>
<p>


    ```ruby
input_bam  ./NA24385_aligned_by_ngmlr_chr21.bam  #specify the bam file path
file_prefix  NA24385_aligned_by_ngmlr_chr21 #file prefix you prefer for output
ref_genome  /data/maiziezhou_lab/Softwares/refdata-hg19-2.1.0/fasta/genome.fa
chr_num  21  # chromosome number (excluding X,Y)
output_dir  ./DipPAV_output/ # specify your prefered output folder
num_bucket  20000000  # number of bucket in LSH step (default = 20000000)
kmer_size 15 # kmer size in LSH step and model training (default = 15)
dim  200  # kmer representation dimension (default = 200)
    ```

</p>
</details>




### Generate step-spefic bash files

DipPAV contains 5 step to generate contigs and call variants. After you edit the input.config, you can run 

python3 jobs_generator.py

Then, you will see DipPAV_step1.sh, DipPAV_step2.sh, DipPAV_step3.sh, DipPAV_step4.sh and DipPAV_step5.sh under the main folder.

You can run the step by 

    ```bash
bash DipPAV_step1.sh
bash DipPAV_step2.sh
bash DipPAV_step3.sh
bash DipPAV_step4.sh
bash DipPAV_step5.sh
    ```


### Check the result

When all steps finish running, you can go to the output folder you specified in "input.config". Under the output folder, you can see phasing_result, word_embedding_result, clustering_result and assembly_result. The contigs file is under "assembly_result/final_contigs/", and the variants file is "assembly_result/final_contigs/variant_call/DipPAV_variants.vcf".




