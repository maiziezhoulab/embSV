from argparse import ArgumentParser
from subprocess import Popen
import os
parser = ArgumentParser(description="",usage='use "python3 %(prog)s --help" for more information')
parser.add_argument('--input_path','-i')
parser.add_argument('--output_dir','-o')
parser.add_argument('--chr_num','-chr',type=int)
parser.add_argument('--ref')

args = parser.parse_args()
input_path = args.input_path
output_dir = args.output_dir
chr_num = args.chr_num
ref_path = args.ref
import os
global code_dir
code_dir=os.path.dirname(os.path.realpath(__file__))+'/'

if not os.path.exists(output_dir):
	os.makedirs(output_dir)

prefix = input_path.split('/')[-1].split('.')[0]

bam_hp1 = output_dir+'/'+prefix+'_hp1.sorted.bam'
bam_hp2 = output_dir+'/'+prefix+'_hp2.sorted.bam'


## diploid variant call

cmd = "svim-asm diploid %s \
   %s \
   %s \
   %s  --query_names"%(output_dir,bam_hp1,bam_hp2,ref_path)
Popen(cmd,shell=True).wait()

## remove false positive

cmd = "python3 %s/vcf_false_positive_filter.py -i %s/variants.vcf -o %s/embSV_variants.vcf"%(code_dir,output_dir,output_dir)
Popen(cmd,shell=True).wait()

