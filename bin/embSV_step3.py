from argparse import ArgumentParser
from subprocess import Popen
import os
parser = ArgumentParser(description="",usage='use "python3 %(prog)s --help" for more information')
parser.add_argument('--chr_num', required=True, help = "required argument")
parser.add_argument('--output_dir','-o', required=True, help = "required argument")
parser.add_argument('--ref_genome','-ref', required=True, help = "required argument")
parser.add_argument('--assembly_threads','-t',default = 10, type=int, help = "optional argument. default= 10")
args = parser.parse_args()
chr_num = args.chr_num
output_dir = args.output_dir
ref_genome = args.ref_genome
assembly_threads = args.assembly_threads

code_dir=os.path.dirname(os.path.realpath(__file__))+'/'
phasing_dir=output_dir+"/phasing_result/"
cluster_dir=output_dir+"/clustering_result/"
assemble_dir=output_dir+"/assembly_result/"
os.system("mkdir -p "+assemble_dir)


# merge phased and unphased fastqs

cmd = "python3 "+code_dir+"/merge_haps.py \
-d1 "+phasing_dir+"/haps_all_phased/ \
-d2 "+cluster_dir+"/fastqs_assigned_unphased/ \
-o "+assemble_dir+"/haps_final_assignment/"
Popen(cmd,shell=True).wait()

# assembly
cmd = "python3 "+code_dir+"/run_assembly.py  \
-i "+assemble_dir+"/haps_final_assignment/ \
-w "+assemble_dir+"/assembly_files/ \
-o "+assemble_dir+"/final_contigs/ \
-p "+phasing_dir+"/pb_info.csv \
-t %d"%(assembly_threads)
Popen(cmd,shell=True).wait()

# data prepare for variant call
cmd = "python3 "+code_dir+"/SVIM-asm_variant_caller_data_prepare.py  \
-i "+assemble_dir+"/final_contigs/final_contig.p_ctg.fa \
-o "+assemble_dir+"/final_contigs/variant_call/ \
-chr "+chr_num+" --ref "+ref_genome
Popen(cmd,shell=True).wait()

# variant call and filter
cmd = "python3 "+code_dir+"/SVIM-asm_variant_caller_variant_call.py  \
-i "+assemble_dir+"/final_contigs/final_contig.p_ctg.fa \
-o "+assemble_dir+"/final_contigs/variant_call/ \
-chr "+chr_num+" --ref "+ref_genome
Popen(cmd,shell=True).wait()


