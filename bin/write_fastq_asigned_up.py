import pysam
import pickle
import os
import numpy as np
from argparse import ArgumentParser
parser = ArgumentParser(description="",usage='use "python3 %(prog)s --help" for more information')
parser.add_argument('--bam_path','-bam')
parser.add_argument('--asign_dict_path','-dc')
parser.add_argument('--output_dir','-o')
parser.add_argument('--difficult_mode','-d', action='store_true')
args = parser.parse_args()
# input_path = args.input_path
bam_path = args.bam_path
asign_dict_path =args.asign_dict_path
output_dir = args.output_dir
difficult_mode = args.output_dir


# samfile = pysam.AlignmentFile("/data/maiziezhou_lab/CanLuo/long_reads_project/chr21_result/phasing_result/NA24385_aligned_by_ngmlr_chr21_phased.bam",'rb')
samfile = pysam.AlignmentFile(bam_path)
samiter = samfile.fetch()

dc = pickle.load(open(asign_dict_path,'rb'))

# output_dir = "/data/maiziezhou_lab/CanLuo/long_reads_project/chr21_result/read_similarity/assigned_unphased_reads/"

if os.path.exists(output_dir):
	os.system("rm -r "+output_dir)
os.system("mkdir "+output_dir)

# first go over dc, if one hp contains over 1000 reads, mark it
if difficult_mode:
	x = np.unique(list(dc.values()),return_counts=True)
	idx =np.argsort(x[1])[::-1]
	pb_sorted =x[0][idx]
	count_sorted = x[1][idx]
	big_pb_list = []
	for i in range(len(count_sorted)):
		if count_sorted[i]>1e3:
			pb = pb_sorted[i]
			if 'hp' in pb:
				pb = '_'.join(pb.split('_')[:-1])
			big_pb_list.append(pb)
	big_pb_list = set(big_pb_list)
else:
	big_pb_list = set()



for read in samiter:
	if read.query_name in dc:
		hp = dc[read.query_name]

		

		# ## to both hap
		# if 'hp' in hp:
		# 	pb = '_'.join(hp.split('_')[:-1])
		# else:
		# 	pb = hp

		# if pb in big_pb_list:
		# 	with open(output_dir+'/'+hp+'.fastq','a+') as f:
		# 		f.write("@"+read.query_name+'\n')
		# 		f.write(read.seq+'\n')
		# 		f.write("+\n")
		# 		f.write(read.qual+'\n')
		# else:
		# 	with open(output_dir+'/'+pb+'_hp1.fastq','a+') as f:
		# 		f.write("@"+read.query_name+'\n')
		# 		f.write(read.seq+'\n')
		# 		f.write("+\n")
		# 		f.write(read.qual+'\n')
		# 	with open(output_dir+'/'+pb+'_hp2.fastq','a+') as f:
		# 		f.write("@"+read.query_name+'\n')
		# 		f.write(read.seq+'\n')
		# 		f.write("+\n")
		# 		f.write(read.qual+'\n')

		#print(hp)
		if 'hp' in hp:
			with open(output_dir+'/'+hp+'.fastq','a+') as f:
				f.write("@"+read.query_name+'\n')
				f.write(read.seq+'\n')
				f.write("+\n")
				f.write(read.qual+'\n')
		else:
			with open(output_dir+'/'+hp+'_hp1.fastq','a+') as f:
				f.write("@"+read.query_name+'\n')
				f.write(read.seq+'\n')
				f.write("+\n")
				f.write(read.qual+'\n')
			with open(output_dir+'/'+hp+'_hp2.fastq','a+') as f:
				f.write("@"+read.query_name+'\n')
				f.write(read.seq+'\n')
				f.write("+\n")
				f.write(read.qual+'\n')








