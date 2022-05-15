chr_num=<chr_num>
output_dir=<output_dir>
ref_genome=<ref_genome>
code_dir=<code_dir>


assemble_dir=${output_dir}/assembly_result/
# data prepare for variant call
source activate /data/maiziezhou_lab/CanLuo/Software/anaconda3/envs/DipPAV
python3 ${code_dir}/SVIM-asm_variant_caller_data_prepare.py  \
       -i ${assemble_dir}/final_contigs/final_contig.p_ctg.fa \
       -o ${assemble_dir}/final_contigs/variant_call/ \
       -chr ${chr_num} --ref ${ref_path}

# variant call and filter
python3 ${code_dir}/SVIM-asm_variant_caller_variant_call.py  \
    -i ${assemble_dir}/final_contigs/final_contig.p_ctg.fa \
    -o ${assemble_dir}/final_contigs/variant_call/ \
    -chr ${chr_num} --ref ${ref_path}


