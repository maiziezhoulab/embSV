from argparse import ArgumentParser
import numpy as np
parser = ArgumentParser(description="",usage='use "python3 %(prog)s --help" for more information')
parser.add_argument('--input_dir','-i')
# parser.add_argument('--output_path','-o')
parser.add_argument('--delete_intermediate_file','-d', action='store_true')
args = parser.parse_args()
input_dir = args.input_dir
# output_path = args.output_path

output_path = input_dir+'/within_haplotype_distances.txt'

tsnecorpath=input_dir+'/TSNE_cords.txt'


def extractBlocks(input):
	s = input.split(",")
	return [[int(s[i]), int(s[i+1])] for i in range(len(s)-1)]

with open(input_dir+'/blocks.txt','r') as f:
	blocks = f.read()
blocks = extractBlocks(blocks)

with open(tsnecorpath,'r') as f:
	s = f.readlines()

cords = []
for line in s:
	cords.append(line[:-1].split(','))

cords = np.array(cords).astype(float)

def get_min_dist(point_cor, point_cor_set):
	distances = np.linalg.norm( point_cor - point_cor_set, ord=2, axis = 1)
	return min(distances)

fw = open(output_path,'w')
max_min_for_4_haps=[]
for range_ in blocks[:-1]:
	cords_set = cords[range_[0]:range_[1]]
	min_dist_set = []
	for i in range(len(cords_set)):
		min_dist = get_min_dist(cords_set[i], np.concatenate([ cords_set[:i],cords_set[i+1:] ]))
		min_dist_set.append(min_dist)
	try:
		max_min_for_4_haps.append(max(min_dist_set))
	except:
		max_min_for_4_haps.append(999)

	min_dist_set = np.array(min_dist_set).astype('str')
	fw.write(','.join(min_dist_set)+'\n')

fw.close()


## reformat nerestneighbor.txt
old_nnpath = input_dir+'/nearestNeighbors.txt'
new_nnapth = input_dir+'/nearestNeighbors.txt'

with open(old_nnpath,'r') as f:
	s = f.readlines()
fw = open(new_nnapth,'w')

for line in s:
	if ("Phase" in line) and ('dist' not in line):
		if "Phase Block 1 Hap 1:" in line:
			line = line[:-2]+"(dist threshold = %.6f):\n"%(max_min_for_4_haps[0])
		elif "Phase Block 1 Hap 2:" in line:
			line = line[:-2]+"(dist threshold = %.6f):\n"%(max_min_for_4_haps[1])
		elif "Phase Block 2 Hap 1:" in line:
			line = line[:-2]+"(dist threshold = %.6f):\n"%(max_min_for_4_haps[2])
		elif "Phase Block 2 Hap 2:" in line:
			line = line[:-2]+"(dist threshold = %.6f):\n"%(max_min_for_4_haps[3])
	
	fw.write(line)

fw.close()




