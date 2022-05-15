###################### input ###########

input_bam=<input_bam>
file_prefix=<file_prefix>
chr_num=<chr_num>
output_dir=<output_dir>
ref_genome=<ref_genome>
code_dir=<code_dir>

############################ phasing ###########
mkdir -p ${output_dir}
phasing_dir=${output_dir}/phasing_result/
mkdir -p ${phasing_dir}

source activate /data/maiziezhou_lab/CanLuo/Software/anaconda3/envs/DipPAV
## phasing
longshot --bam ${input_bam} \
    --ref  ${ref_genome} \
    --out ${phasing_dir}/${file_prefix}_phased.vcf \
    -O ${phasing_dir}/${file_prefix}_phased.bam -F

# index phased bam file
samtools index ${phasing_dir}/${file_prefix}_phased.bam

# phasing infor 
python3 ${code_dir}/get_pb.py \
    -i ${phasing_dir}/${file_prefix}_phased.bam \
    -o ${phasing_dir}/pb_info.csv

# extract phased fastqs
python3 ${code_dir}/write_fastq.py \
    -i ${phasing_dir}/${file_prefix}_phased.bam \
    -o ${phasing_dir}/haps_all_phased/ \
    -p ${phasing_dir}/pb_info.csv

### prepare training information
python3 ${code_dir}/prepare_realign_info.py  \
    -i ${phasing_dir}/${file_prefix}_phased.bam \
    -p ${phasing_dir}/pb_info.csv \
    -o ${phasing_dir}/ 

## reverse read pbs file
python3 ${code_dir}/reverse_read_pb.py \
    -i ${phasing_dir}/reads_pb.p \
    -o ${phasing_dir}/pb_reads.p

# extract phased reads dict
python3 ${code_dir}/extract_read_pb_og.py \
    -i ${phasing_dir}/${file_prefix}_phased.bam \
    -pb ${phasing_dir}/phase_block_info.p \
    -o ${phasing_dir}/read_hp_og.p
