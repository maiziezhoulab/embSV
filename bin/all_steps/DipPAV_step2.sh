###################### input ###########

file_prefix=<file_prefix>
output_dir=<output_dir>
code_dir=<code_dir>
num_bucket=<num_bucket>
kmer_size=<kmer_size>
dim=<dim>

############################ hashing

# prepare environment
source activate  /data/maiziezhou_lab/CanLuo/Software/anaconda3/envs/LSHvec
phasing_dir=${output_dir}/phasing_result/
lshvec_dir=${code_dir}/LSHVec/
lsh_dict=${lshvec_dir}/lshdict/lsh.hash.lsh.pkl
hash_dir=${output_dir}/word_embedding_result/hash_k${kmer_size}_b${num_bucket}/
mkdir -p ${hash_dir}


# bam to seq
python3 ${code_dir}/bamtoseq.py \
    -i ${phasing_dir}/${file_prefix}_phased.bam \
    -o ${hash_dir}/${file_prefix}.seq


# seq to names
cut -f 2  ${hash_dir}/${file_prefix}.seq \
    > ${hash_dir}/${file_prefix}.name 

# hashing reads
python3.7 ${lshvec_dir}/scripts/fastseq/hashSeq.py \
    -i ${hash_dir}/${file_prefix}.seq \
    --hash lsh  \
    --lsh_file ${lsh_dict} \
    -o ${hash_dir}/lsh.hash \
    -k ${kmer_size} --bucket ${num_bucket}

############################ model training

model_dir=${output_dir}/word_embedding_result/model_k${kmer_size}_b${num_bucket}_dim${dim}/
mkdir -p ${model_dir}

# model training 

${lshvec_dir}/lshvec skipgram \
    -input ${hash_dir}/lsh.hash \
    -output ${model_dir}/mod \
    -minCount 1 -dim ${dim} 

# Extract embedding
python3.7 ${code_dir}/embedder_v2.py \
    --model_path ${model_dir}/mod.bin \
    --hash_path ${hash_dir}/lsh.hash \
    --read_name_path ${hash_dir}/${file_prefix}.name  \
    -o ${model_dir}/embeds.emb


