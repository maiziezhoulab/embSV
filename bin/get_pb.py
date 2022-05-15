import pysam 
import pickle
import pandas as pd
from argparse import ArgumentParser
parser = ArgumentParser(description="Author: xzhou15@cs.stanford.edu\n",usage='use "python3 %(prog)s --help" for more information')
parser.add_argument('--input_path','-i')
parser.add_argument('--output_path','-o')
args = parser.parse_args()
output_path = args.output_path
bam_path = args.input_path

samfile = pysam.AlignmentFile(bam_path)
samiter = samfile.fetch()
pb_inf = {}

for read in samiter:
	tags = read.get_tags()
	phased_flag = 0
	hp = -1
	pb = -1
	for tag in tags:
		if tag[0]=='HP':
			phased_flag=1
			hp = tag[1]
		if tag[0]=='PS':
			pb = tag[1]
	if phased_flag:
		if pb in pb_inf:
			pb_inf[pb].append(read.pos)
		else:
			pb_inf[pb] = [read.pos]

pb_list = []
for pb in pb_inf:
	poss = pb_inf[pb]
	pb_inf[pb]=(min(poss),max(poss))
	pb_list.append((pb,min(poss),max(poss)))

				

df = pd.DataFrame(pb_list,columns = ['name','start','end'])
df.to_csv(output_path,index=False)









