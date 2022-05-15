from argparse import ArgumentParser
import pickle
parser = ArgumentParser(description="",usage='use "python3 %(prog)s --help" for more information')
parser.add_argument('--input_path','-i')
parser.add_argument('--output_path','-o')
parser.add_argument('--read_pb_og','-dc')
parser.add_argument('--delete_intermediate_file','-d', action='store_true')
args = parser.parse_args()
input_path = args.input_path
output_path = args.output_path
read_pb_og = args.read_pb_og
dc_og = pickle.load(open(read_pb_og, 'rb'))

with open(input_path,'r') as f:
	s =f.readlines()


name_list = []
dist_list = []
contig_list = []
for i in range(len(s)):
	line = s[i]
	if 'ccs\n' in line :
		name_list.append(line[:-1])
		
	elif "Phase" in line:
		if 'ccs,' in s[i+1]:
			dist_list.append(eval(s[i+1].split(', ')[1][:-1]))
		else:
			dist_list.append(999)
		contig_list.append(s[i+1].split(', ')[0])

dc ={}
#print(name_list)
for i in range(len(name_list)):
	dist_for_this_name = dist_list[i*4:i*4+4]
	contigs_for_this_name = contig_list[i*4:i*4+4]
	if min(dist_for_this_name)!=999:
		min_idx = dist_for_this_name.index(min(dist_for_this_name))
		contig = contigs_for_this_name[min_idx]
		# print(name_list[i],contig)
		dc[name_list[i]]=dc_og[contig]

# print(dc)
print(len(name_list),len(contig_list),len(dist_list))
print(name_list[:10])
print(contig_list[:10],contig_list[-10:])
print(dist_list[:10],dist_list[-10:])
pickle.dump(dc,open(output_path,'wb'))