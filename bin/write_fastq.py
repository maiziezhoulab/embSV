import pysam
import pickle
import os
import pandas as pd
from argparse import ArgumentParser
parser = ArgumentParser(description="Author: xzhou15@cs.stanford.edu\n",usage='use "python3 %(prog)s --help" for more information')
parser.add_argument('--input_path','-i')
parser.add_argument('--output_dir','-o')
parser.add_argument('--pb_info_path','-p')
args = parser.parse_args()
output_dir = args.output_dir
bam_path = args.input_path
pb_info_path = args.pb_info_path


# load samfile
samfile = pysam.AlignmentFile(bam_path)
samiter = samfile.fetch()

# load pb information
df = pd.read_csv(pb_info_path)
pb_dict = {}
for i in range(df.shape[0]):
	pb_name = df['name'][i]
	pb_start = df['start'][i]
	pb_end = df['end'][i]
	pb_str = 'PS%d_%d_%d'%(pb_name,pb_start,pb_end)
	pb_dict[pb_name]=pb_str



if not os.path.exists(output_dir):
	os.makedirs(output_dir)
else:
	os.system("rm -r %s"%output_dir)
	os.makedirs(output_dir)

write_dict={}

for read in samiter:
	tags = read.get_tags()
	phase_flag = 0
	hp =999
	pb =999
	for tag in tags:
		if tag[0]=='HP':
			phase_flag=1
			hp = tag[1]
		if tag[0]=='PS':
			pb = tag[1]

	if phase_flag:
		pb_str=pb_dict[pb]
		hp = pb_str+'_hp'+str(hp)
		if hp in write_dict:
			if read.query_name not in write_dict[hp]:
				output_path = output_dir+'/'+hp+'.fastq'
				seq = read.seq
				qual = read.qual
				with open(output_path,'a+') as f:
					f.write("@"+read.query_name+'\n'+\
						seq+'\n'+\
						'+\n'+\
						qual+'\n')
				write_dict[hp] = write_dict[hp]|{read.query_name}
		else:
			output_path = output_dir+'/'+hp+'.fastq'
			seq = read.seq
			qual = read.qual
			with open(output_path,'a+') as f:
				f.write("@"+read.query_name+'\n'+\
					seq+'\n'+\
					'+\n'+\
					qual+'\n')
			write_dict[hp] = {read.query_name}

















