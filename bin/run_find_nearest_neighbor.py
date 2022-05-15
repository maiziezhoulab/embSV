from argparse import ArgumentParser
import multiprocessing as mp
import pandas as pd
import pickle
from subprocess import Popen
import os
import time
from multiprocessing import Pool,cpu_count,active_children,Manager

parser = ArgumentParser(description="",usage='use "python3 %(prog)s --help" for more information')
parser.add_argument('--num_of_threads','-t',type=int,default = 10)
parser.add_argument('--input_path','-i')
parser.add_argument('--output_dir','-o')
parser.add_argument('--emb_phased_dir','-phased')
parser.add_argument('--emb_unphased_dir','-unphased')
parser.add_argument('--n_threads_TSNE','-threadsT',type = int, default = 10)
parser.add_argument('--delete_intermediate_file','-d', action='store_true')
parser.add_argument('--split','-sp',type=int)
args = parser.parse_args()
num_of_threads = args.num_of_threads
input_path = args.input_path
output_dir = args.output_dir
emb_unphased = args.emb_unphased_dir
emb_contig = args.emb_phased_dir
split = args.split
n_threads_TSNE = args.n_threads_TSNE

import os
global code_dir
code_dir=os.path.dirname(os.path.realpath(__file__))+'/'

with open(input_path, "rb") as f:
    dc_pb_reads = pickle.load(f)

# dc_pb_reads = pickle.load(open(input_path,'rb'))

os.system("mkdir "+output_dir)


# os.system("rm "+input_dir+'/progress.log')
# os.system("rm "+input_dir+'/stats.log')


def calculation_task(input_path,output_dir ,emb_contig,emb_unphased,start_idx,end_idx,n_threads_TSNE,code_dir):
	cmd = "python3.7 %s/find_nearest_neighbor_batch_tasks.py \
-i %s \
-o %s \
-contig %s \
-unphased %s \
-start %d -end %d -threadsT %d"%(code_dir,input_path,output_dir,emb_contig,emb_unphased,start_idx,end_idx,n_threads_TSNE)
	Popen(cmd,shell=True).wait()
	print(cmd,'=============')
	return 

#/data/maiziezhou_lab/CanLuo/long_reads_project/chr1_result/realign/up_bothhp/final_contigs/training_consistent_lsh/mod.bin

total_num = split

task_per_batch = int(len(dc_pb_reads)/split)
print(len(dc_pb_reads),split,task_per_batch)

if num_of_threads==1:
	for i in range(split):
		if i<split-1:
			start_idx = i*task_per_batch
			end_idx = (i+1)*task_per_batch		
		else:
			start_idx = i*task_per_batch
			end_idx = len(dc_pb_reads)
		calculation_task(input_path,output_dir ,emb_contig,emb_unphased,start_idx,end_idx,n_threads_TSNE,code_dir)

else:
	pool = mp.Pool(num_of_threads)
	count = 1
	print("============================")
	print("\n\n")
	print("parelleling now, num of threads: %d"%(num_of_threads))
	print("\n\n")
	print("============================")
	for i in range(split):
		count+=1
		if i<split-1:
			start_idx = i*task_per_batch
			end_idx = (i+1)*task_per_batch		
		else:
			start_idx = i*task_per_batch
			end_idx = len(dc_pb_reads)
		print(i,start_idx,end_idx)
		pool.apply_async(calculation_task,args=(input_path,output_dir ,emb_contig,emb_unphased,start_idx,end_idx,n_threads_TSNE,code_dir))
		print("submit %d"%(count-1))
		if (count - 1)%num_of_threads == 0 or (count - 1) == total_num:
			pool.close()
			while len(active_children()) > 1:
				time.sleep(0.5)
			pool.join()

			if (count - 1) == total_num:
				print("finished all calculation" )
			else:
				pool = Pool(num_of_threads)








