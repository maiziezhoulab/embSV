###################### input 

output_dir=<output_dir>
code_dir=<code_dir>

# #######################################################


#                  assembly


# #######################################################
phasing_dir=${output_dir}/phasing_result/
cluster_dir=${output_dir}/clustering_result/

assemble_dir=${output_dir}/assembly_result/
mkdir -p ${assemble_dir}

source activate /data/maiziezhou_lab/CanLuo/Software/anaconda3/envs/DipPAV

# merge phased and unphased fastqs

python3 ${code_dir}/merge_haps.py \
    -d1 ${phasing_dir}/haps_all_phased/ \
    -d2 ${cluster_dir}/fastqs_assigned_unphased/ \
    -o ${assemble_dir}/haps_final_assignment/


# assembly
python3 ${code_dir}/run_assembly.py  \
    -i ${assemble_dir}/haps_final_assignment/ \
    -w ${assemble_dir}/assembly_files/ \
    -o ${assemble_dir}/final_contigs/ \
    -p ${phasing_dir}/pb_info.csv \
    -t 10




