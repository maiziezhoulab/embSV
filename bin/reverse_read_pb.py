from argparse import ArgumentParser
import pickle
parser = ArgumentParser(description="",usage='use "python3 %(prog)s --help" for more information')
parser.add_argument('--input_path','-i')
parser.add_argument('--output_path','-o')
parser.add_argument('--delete_intermediate_file','-d', action='store_true')
args = parser.parse_args()
input_path = args.input_path
output_path = args.output_path

dc = pickle.load(open(input_path,'rb'))

dc1 = {}
for read in dc :
	pbs=dc[read]
	pb1 = 'PS%d_%d_%d'%(pbs[0][0],pbs[0][-2],pbs[0][-1])
	pb2 = 'PS%d_%d_%d'%(pbs[1][0],pbs[1][-2],pbs[1][-1])
	if pbs[0][0]<pbs[1][0]:
		pbs = (pb1,pb2)
	else:
		pbs = (pb2,pb1)
	dc[read]=pbs
	if pbs in dc1:
		dc1[pbs].append(read)
	else:
		dc1[pbs]=[read]
print(len(dc1))
pickle.dump(dc1,open(output_path,'wb'))
	