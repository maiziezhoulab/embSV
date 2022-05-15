import pysam
import pickle
import os
import pandas as pd
from argparse import ArgumentParser
parser = ArgumentParser(description="Author: xzhou15@cs.stanford.edu\n",usage='use "python3 %(prog)s --help" for more information')
parser.add_argument('--input_path','-i')
parser.add_argument('--output_path','-o')
# parser.add_argument('--pb_info_path','-p')
args = parser.parse_args()
output_path = args.output_path
bam_path = args.input_path
# pb_info_path = args.pb_info_path


# load samfile
samfile = pysam.AlignmentFile(bam_path)
samiter = samfile.fetch()

# load pb information
# df = pd.read_csv(pb_info_path)
# pb_dict = {}
# for i in range(df.shape[0]):
# 	pb_name = df['name'][i]
# 	pb_start = df['start'][i]
# 	pb_end = df['end'][i]
# 	pb_str = 'PS%d_%d_%d'%(pb_name,pb_start,pb_end)
# 	pb_dict[pb_name]=pb_str



os.system("rm  %s"%output_path)

write_name = []
i = 0
for read in samiter:
	i+=1

	read_name = read.query_name
	seq = read.seq
	with open(output_path,'a+') as f:
		f.write("%d\t"%i+read.query_name+'\t'+\
			seq+'\n')
