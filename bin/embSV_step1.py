from argparse import ArgumentParser
from subprocess import Popen
import os
parser = ArgumentParser(description="",usage='use "python3 %(prog)s --help" for more information')
parser.add_argument('--input_bam','-i', required=True, help = "required argument")
parser.add_argument('--file_prefix','-px', required=True, help = "required argument")
parser.add_argument('--chr_num', required=True, help = "required argument")
parser.add_argument('--output_dir','-o', required=True, help = "required argument")
parser.add_argument('--ref_genome','-ref', required=True, help = "required argument")
args = parser.parse_args()
input_bam = args.input_bam
file_prefix = args.file_prefix
chr_num = args.chr_num
output_dir = args.output_dir
ref_genome = args.ref_genome

code_dir=os.path.dirname(os.path.realpath(__file__))+'/'

os.system("mkdir -p "+output_dir)
phasing_dir=output_dir+"/phasing_result/"
os.system("mkdir -p "+phasing_dir)


## phasing
cmd = "longshot --bam "+input_bam+" \
--ref  "+ref_genome+" \
--out "+phasing_dir+"/"+file_prefix+"_phased.vcf \
-O "+phasing_dir+"/"+file_prefix+"_phased.bam -F"
Popen(cmd,shell=True).wait()

# index phased bam file
cmd = "samtools index "+phasing_dir+"/"+file_prefix+"_phased.bam"
Popen(cmd,shell=True).wait()

# phasing infor 
cmd = "python3 "+code_dir+"/get_pb.py \
-i "+phasing_dir+"/"+file_prefix+"_phased.bam \
-o "+phasing_dir+"/pb_info.csv"
Popen(cmd,shell=True).wait()

# extract phased fastqs
cmd = "python3 "+code_dir+"/write_fastq.py \
-i "+phasing_dir+"/"+file_prefix+"_phased.bam \
-o "+phasing_dir+"/haps_all_phased/ \
-p "+phasing_dir+"/pb_info.csv"
Popen(cmd,shell=True).wait()

### prepare training information
cmd = "python3 "+code_dir+"/prepare_realign_info.py  \
-i "+phasing_dir+"/"+file_prefix+"_phased.bam \
-p "+phasing_dir+"/pb_info.csv \
-o "+phasing_dir+"/"
Popen(cmd,shell=True).wait()

## reverse read pbs file
cmd = "python3 "+code_dir+"/reverse_read_pb.py \
-i "+phasing_dir+"/reads_pb.p \
-o "+phasing_dir+"/pb_reads.p"
Popen(cmd,shell=True).wait()

# extract phased reads dict
cmd = "python3 "+code_dir+"/extract_read_pb_og.py \
-i "+phasing_dir+"/"+file_prefix+"_phased.bam \
-pb "+phasing_dir+"/phase_block_info.p \
-o "+phasing_dir+"/read_hp_og.p"
Popen(cmd,shell=True).wait()




