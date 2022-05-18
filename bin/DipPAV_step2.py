from argparse import ArgumentParser
from subprocess import Popen
import os
parser = ArgumentParser(description="",usage='use "python3 %(prog)s --help" for more information')
parser.add_argument('--file_prefix','-px', required=True, help = "required argument")
parser.add_argument('--output_dir','-o', required=True, help = "required argument")
parser.add_argument('--num_bucket','-b',default = 20000000, type =int, help = "optional argument. range(5000, 20000000). default= 20000000")
parser.add_argument('--kmer_size','-k', default = 15, type =int, help = "optional argument. default= 15")
parser.add_argument('--dim','-dim',default = 200, type =int, help = "optional argument. default= 200")
parser.add_argument('--clustering_task_split','-split',default = 60, type = int, help = "optional argument. default= 60")
parser.add_argument('--clustering_threads','-t',default = 10, type =int, help = "optional argument. default= 10")

args = parser.parse_args()
file_prefix = args.file_prefix
output_dir = args.output_dir
num_bucket = args.num_bucket
kmer_size = args.kmer_size
dim = args.dim
clustering_task_split = args.clustering_task_split
clustering_threads = args.clustering_threads


code_dir=os.path.dirname(os.path.realpath(__file__))+'/'

phasing_dir=output_dir+"/phasing_result/"
lshvec_dir=code_dir+"/LSHVec/"
lsh_dict=lshvec_dir+"/lshdict/lsh.hash.lsh.pkl"



# #######################################################
#
#
#                  hashing
#
#
# ######################################################
hash_dir=output_dir+"/word_embedding_result/hash_k"+str(kmer_size)+"_b"+str(num_bucket)+'/'
os.system("mkdir -p "+hash_dir)

# bam to seq
cmd = "python3 "+code_dir+"/bamtoseq.py \
-i "+phasing_dir+"/"+file_prefix+"_phased.bam \
-o "+hash_dir+"/"+file_prefix+".seq"
Popen(cmd,shell=True).wait()

# seq to names
cmd = "cut -f 2  "+hash_dir+"/"+file_prefix+".seq \
> "+hash_dir+"/"+file_prefix+".name "
Popen(cmd,shell=True).wait()

# hashing reads
cmd = "python3.7 "+lshvec_dir+"/scripts/fastseq/hashSeq.py \
-i "+hash_dir+"/"+file_prefix+".seq \
--hash lsh  \
--lsh_file "+lsh_dict+" \
-o "+hash_dir+"/lsh.hash \
-k "+str(kmer_size)+" --bucket "+str(num_bucket)
Popen(cmd,shell=True).wait()

# #######################################################
#
#
#                  model training
#
#
# ######################################################

model_dir=output_dir+"/word_embedding_result/model_k"+str(kmer_size)+"_b"+str(num_bucket)+"_dim"+str(dim)+"/"
os.system("mkdir -p "+model_dir)

# model training 

cmd = lshvec_dir+"/lshvec skipgram \
-input "+hash_dir+"/lsh.hash \
-output "+model_dir+"/mod \
-minCount 1 -dim "+str(dim)
Popen(cmd,shell=True).wait()

# Extract embedding
cmd = "python3.7 "+code_dir+"/embedder_v2.py \
--model_path "+model_dir+"/mod.bin \
--hash_path "+hash_dir+"/lsh.hash \
--read_name_path "+hash_dir+"/"+file_prefix+".name  \
-o "+model_dir+"/embeds.emb"
Popen(cmd,shell=True).wait()

# #######################################################
#
#
#                  clustering
#
#
# ######################################################
cluster_dir=output_dir+"/clustering_result/"
os.system("mkdir -p "+cluster_dir)

## data preparation

# split unphased reads embedding
cmd = "python3 "+code_dir+"/split_unphased_emb.py \
-i "+model_dir+"/embeds.emb \
-o "+cluster_dir+"/unphased_reads_embedding/ \
-dc "+phasing_dir+"/reads_pb.p"
Popen(cmd,shell=True).wait()

# split phased reads embedding
cmd = "python3 "+code_dir+"/split_original_phased_read_emb.py \
-i "+model_dir+"/embeds.emb \
-o "+cluster_dir+"/phased_reads_embedding/ \
-dc "+phasing_dir+"/read_hp_og.p"
Popen(cmd,shell=True).wait()

###clustering 

cmd = "python3 "+code_dir+"/run_find_nearest_neighbor.py \
 -i "+phasing_dir+"/pb_reads.p \
 -o "+cluster_dir+"/nearestNeighbor/ \
 -phased "+cluster_dir+"/phased_reads_embedding/ \
 -unphased "+cluster_dir+"/unphased_reads_embedding/ \
 --split %d -t %d" %(clustering_task_split,clustering_threads)
Popen(cmd,shell=True).wait()

## result reformatting

# collect nn result
cmd = "cat "+cluster_dir+"/nearestNeighbor/*/*/nearestNeighbors.txt \
> "+cluster_dir+"/nearestNeighbor/nearestNeighbors.txt"
Popen(cmd,shell=True).wait()

# extract unphased reads assignment info
cmd = "python3 "+code_dir+"/extract_up_assign.py \
-i "+cluster_dir+"/nearestNeighbor/nearestNeighbors.txt \
-o "+cluster_dir+"/nearestNeighbor/nearestNeighbors.p \
-dc "+phasing_dir+"/read_hp_og.p"
Popen(cmd,shell=True).wait()

# write assigned unphased reads
cmd = "python3 "+code_dir+"/write_fastq_asigned_up.py \
-bam "+phasing_dir+"/"+file_prefix+"_phased.bam \
-o  "+cluster_dir+"/fastqs_assigned_unphased/ \
-dc "+cluster_dir+"/nearestNeighbor/nearestNeighbors.p"
Popen(cmd,shell=True).wait()
















