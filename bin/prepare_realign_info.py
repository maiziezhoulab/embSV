import pysam 
import os
import pandas as pd
from subprocess import Popen
from argparse import ArgumentParser
import pickle
parser = ArgumentParser()
parser.add_argument("--input_bam","-i")
parser.add_argument("--pb_info_csv","-p")
parser.add_argument("--output_dir",'-o')

args = parser.parse_args()
input_bam = args.input_bam
output_dir = args.output_dir
pb_info_csv = args.pb_info_csv

if not os.path.exists(output_dir):
	os.makedirs(output_dir)

# write pb info dict
df = pd.read_csv(pb_info_csv)
pb_dict = {}

for i in range(df.shape[0]):
	name = df['name'][i]
	start = df['start'][i]
	end = df['end'][i]
	pb_dict[str(name)]=(start,end)

pickle.dump(pb_dict,open(output_dir+'/phase_block_info.p','wb'))


# write uncovered_reads.p
samfile = pysam.AlignmentFile(input_bam)
samiter = samfile.fetch()
phased_reads = set()
uncover_dict = {}
for read in samiter:
	phase_flag = 0
	tags = read.get_tags()
	read_name = read.query_name
	for tag in tags:
		if tag[0]=='HP':
			phase_flag=1
			break

	if phase_flag:
		phased_reads = phased_reads|{read_name}
	elif read_name not in phased_reads:
		start = read.pos 
		end = read.reference_end
		#seq = read.seq
		uncover_dict[read_name]=[start,end]

print(len(uncover_dict))
pickle.dump(uncover_dict,open(output_dir+'/uncovered_reads.p','wb'))

# find 2 most close phase blocks for each uncovered read

read_asign_dict = {}
for read in uncover_dict:
	read_start = uncover_dict[read][0]
	read_end = uncover_dict[read][1]

	dist_list = []
	pb_dist_dict = {}
	for pb in pb_dict:
		pb_start = pb_dict[pb][0]
		pb_end = pb_dict[pb][1]
		dist = max(pb_start,read_start)-min(pb_end,read_end)
		dist_list.append([pb,dist])
		pb_dist_dict[pb]=dist
	df_dist = pd.DataFrame(dist_list,columns = ['pb','dist'])
	df_dist_sorted = df_dist.sort_values('dist').reset_index(drop=True)
	if df_dist_sorted.shape[0]>1:
		asign_pbs = df_dist_sorted.pb[:2].tolist()
	else:
		asign_pbs = [df_dist_sorted.pb[0]]
	asign_list = []

	for pb in asign_pbs:
		asign_info = [int(pb), pb_dist_dict[pb],read_start,read_end,pb_dict[pb][0],pb_dict[pb][1]]
		asign_list.append(asign_info)

	read_asign_dict[read]=asign_list

pickle.dump(read_asign_dict,open(output_dir+'/reads_pb.p','wb'))





























