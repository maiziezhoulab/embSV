
###################### input 

file_prefix=<file_prefix>
output_dir=<output_dir>
code_dir=<code_dir>
num_bucket=<num_bucket>
kmer_size=<kmer_size>
dim=<dim>

# #######################################################


#                  clustering



# #######################################################
# prepare environment
source activate /data/maiziezhou_lab/CanLuo/Software/anaconda3/envs/DipPAV

phasing_dir=${output_dir}/phasing_result/
model_dir=${output_dir}/word_embedding_result/model_k${kmer_size}_b${num_bucket}_dim${dim}/
cluster_dir=${output_dir}/clustering_result/
mkdir -p ${cluster_dir}

## data preparation

# split unphased reads embedding
python3 ${code_dir}/split_unphased_emb.py \
    -i ${model_dir}/embeds.emb \
    -o ${cluster_dir}/unphased_reads_embedding/ \
    -dc ${phasing_dir}/reads_pb.p

# split phased reads embedding
python3 ${code_dir}/split_original_phased_read_emb.py \
    -i ${model_dir}/embeds.emb \
    -o ${cluster_dir}/phased_reads_embedding/ \
    -dc ${phasing_dir}/read_hp_og.p

###clustering 

python3 ${code_dir}/run_find_nearest_neighbor.py \
    -i ${phasing_dir}/pb_reads.p \
    -o ${cluster_dir}/nearestNeighbor/ \
    -phased ${cluster_dir}/phased_reads_embedding/ \
    -unphased ${cluster_dir}/unphased_reads_embedding/ \
    --split 1 -t 1 

## result reformatting

# collect nn result
cat ${cluster_dir}/nearestNeighbor/*/*/nearestNeighbors.txt > ${cluster_dir}/nearestNeighbor/nearestNeighbors.txt

# extract unphased reads assignment info
python3 ${code_dir}/extract_up_assign.py \
    -i ${cluster_dir}/nearestNeighbor/nearestNeighbors.txt \
    -o ${cluster_dir}/nearestNeighbor/nearestNeighbors.p \
    -dc ${phasing_dir}/read_hp_og.p

# write assigned unphased reads
python3 ${code_dir}/write_fastq_asigned_up.py \
    -bam ${phasing_dir}/${file_prefix}_phased.bam \
    -o  ${cluster_dir}/fastqs_assigned_unphased/ \
    -dc ${cluster_dir}/nearestNeighbor/nearestNeighbors.p 

