from argparse import ArgumentParser
import pickle
import os
from subprocess import Popen
import numpy as np
parser = ArgumentParser(description="",usage='use "python3 %(prog)s --help" for more information')
parser.add_argument('--input_path','-i')
parser.add_argument('--output_dir','-o')
parser.add_argument('--start_idx','-start',type = int)
parser.add_argument('--end_idx','-end',type = int)
parser.add_argument('--emb_contig','-contig')
parser.add_argument('--emb_unphased','-unphased')
parser.add_argument('--n_threads_TSNE','-threadsT',type = int, default = 10)
parser.add_argument('--delete_intermediate_file','-d', action='store_true')
args = parser.parse_args()
input_path = args.input_path
output_dir = args.output_dir
emb_unphased = args.emb_unphased
emb_contig = args.emb_contig
start_idx = args.start_idx
end_idx = args.end_idx
output_dir = output_dir+'/%d_%d'%(start_idx,end_idx)
n_threads_TSNE = args.n_threads_TSNE

import os
global code_dir
code_dir=os.path.dirname(os.path.realpath(__file__))+'/'

def get_num_of_lines(input_path):
	os.system("touch "+input_path)
	with open(input_path,'r') as f:
		s = f.readlines()

	return len(s)
with open(input_path, "rb") as f:
    dc = pickle.load(f)
# dc = pickle.load(open(input_path,'rb'))

os.system("mkdir "+output_dir)
i= 0
for pbs in dc:
	if i>=start_idx and i< end_idx:
		
		# print("===============",i,"=============")
		pb1 = pbs[0]
		pb2 = pbs[1]
		pb1_hp1 = pb1+'_hp1'
		pb1_hp2 = pb1+'_hp2'
		pb2_hp1 = pb2+'_hp1'
		pb2_hp2 = pb2+'_hp2'

		unphased_path = emb_unphased+'/'+pb1+'and'+pb2+'.emb'
		pb1_hp1_path = emb_contig+'/'+pb1_hp1+'.emb'
		pb1_hp2_path = emb_contig+'/'+pb1_hp2+'.emb'
		pb2_hp1_path = emb_contig+'/'+pb2_hp1+'.emb'
		pb2_hp2_path = emb_contig+'/'+pb2_hp2+'.emb'

		unphased_lines = get_num_of_lines(unphased_path)
		pb1_hp1_lines = get_num_of_lines(pb1_hp1_path)
		pb1_hp2_lines = get_num_of_lines(pb1_hp2_path)
		pb2_hp1_lines = get_num_of_lines(pb2_hp1_path)
		pb2_hp2_lines = get_num_of_lines(pb2_hp2_path)
		# print(pb1_hp1_path,pb1_hp2_path,pb2_hp1_path,pb2_hp2_path,unphased_path)
		pbs_dir = output_dir+'/'+pb1+'and'+pb2+'/'
		os.system("mkdir "+pbs_dir)


		cmd = "cat %s %s %s %s %s > %s/embeds.emb"%(pb1_hp1_path,pb1_hp2_path,pb2_hp1_path,pb2_hp2_path,unphased_path, pbs_dir)
		os.system(cmd)

		lines = np.array([pb1_hp1_lines,pb1_hp2_lines,pb2_hp1_lines,pb2_hp2_lines,unphased_lines])

		cmd = "python3.7 %s/neighborer.py  \
		%s/embeds.emb \
		%s/nearestNeighbors.txt \
		0,%d,%d,%d,%d,%d \
		%s/TSNECluster.pdf"%(code_dir,pbs_dir,pbs_dir,
			lines[:1].sum(),lines[:2].sum(),lines[:3].sum(),lines[:4].sum(),lines[:5].sum(),
			pbs_dir)
		# print(cmd)
		Popen(cmd,shell=True).wait()
		## calculate within haplotype distance
		cmd  = "python3.7 %s/calculate_within_haplotype_distance_threshold.py \
		-i %s"%(code_dir,pbs_dir)
		Popen(cmd,shell=True).wait()


		print(pbs,"done")
	i+=1
		# break





