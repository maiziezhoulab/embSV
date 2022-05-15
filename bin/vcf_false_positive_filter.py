from argparse import ArgumentParser
import jellyfish
parser = ArgumentParser(description="",usage='use "python3 %(prog)s --help" for more information')
parser.add_argument('--input_path','-i')
parser.add_argument('--output_path','-o')
parser.add_argument('--delete_intermediate_file','-d', action='store_true')
args = parser.parse_args()
input_path = args.input_path
output_path = args.output_path



with open(input_path,'r') as f:
	s = f.readlines()


# get vcf dict
dc = {}
header = []
for line in s:
	if line[0]=='#':
		header.append(line)
	else:

		data = line.split('\t')
		
		sv_type = data[7].split(';')[0].split('=')[1]
		if sv_type in {"INS","DEL"}:

			sv_length = abs(int(data[7].split(';')[2].split('=')[1]))
			signature = (data[0],data[1],sv_type)
			if signature not in dc:
				dc[signature] = [[sv_length , line]]
			else:
				dc[signature].append([sv_length , line])
		else:
			signature = (data[0],data[1],sv_type)
			dc[signature] = [['none' , line]]


print(len(s)-len(header),len(dc))

## merge sv
merged_sv_list = []
for sv_sig in dc:
	if len(dc[sv_sig])==1:
		max_sv = dc[sv_sig][0][1]
	else:
		all_sv = dc[sv_sig]
		max_len = all_sv[0][0]
		max_sv = all_sv[0][1]

		for i in range(1,len(all_sv)):
			new_len = all_sv[i][0]
			if new_len>max_len:
				max_len = new_len
				max_sv = all_sv[i][1]
	merged_sv_list.append(max_sv)


vcf_v2 = merged_sv_list

# merge more



def extract_line_info(line):
	data = line.split('\t')
	# print(data)
	sv_type = data[7].split(';')[0].split('=')[1]
	if sv_type in {"INS","DEL"}:
		sv_length = abs(int(data[7].split(';')[2].split('=')[1]))
	else:
		sv_length = 'none'
	chr_name = data[0]
	pos = int(data[1])
	pbs = data[7].split(';')[-1].split(',')
	pbs = [ '_'.join(contig.split('_')[:-2]) for contig in pbs]
	if sv_type=='DEL':
		seq = data[3]
	elif sv_type=='INS':
		seq = data[4]
	else:
		seq = 'none'
	return [sv_type,chr_name,pos,seq,pbs,sv_length]


def check_merge_or_not(line1,line2):
	data1=extract_line_info(line1)
	data2=extract_line_info(line2)
	merge_flag = 0
	out_range_flag = 0
	if data1[0] in {"INS","DEL"}:
		if data1[:2]==data2[:2]:
			if abs(data1[2]-data2[2])>700:
				out_range_flag =1
				return ["out of range",line2]
			else:
				sim = jellyfish.jaro_distance(data1[3],data2[3])
				if sim>0.65:
					# if len(set(data1[4])&set(data2[4]))>0:
					if 1:
						merge_flag = 1
						if data1[5]>data2[5]:
							merged_line = line1
						else:
							merged_line = line2


	if merge_flag:
		return ["merge",merged_line]
	else:
		return ["dont merge",line2]


new_sv = [merged_sv_list[0]]
m = 0
for i in range(1,len(merged_sv_list)):
	# print(i)
	merge_flag = 0
	for j in range(len(new_sv)-1,0,-1):
		# [sv_type,chr_name,pos,seq,pbs,sv_length]
		merge_check_result = check_merge_or_not(new_sv[j],merged_sv_list[i])
		if merge_check_result[0]=='merge':
			merge_flag = 1
			print("merge")
			m+=1
			new_sv[j]=merge_check_result[1]
		elif merge_check_result[0]=='out of range':
			break
	if merge_flag==0:
		new_sv.append(merged_sv_list[i])


## write down new vcf
print("merge: ",m)
with open(output_path,'w') as f:
	f.writelines(header+new_sv)












	


