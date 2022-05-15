from argparse import ArgumentParser
import ast
import os
import pickle
parser = ArgumentParser(description="",usage='use "python3 %(prog)s --help" for more information')
parser.add_argument('--input_path','-i')
parser.add_argument('--output_dir','-o')
parser.add_argument('--read_pb_path','-dc')
parser.add_argument('--delete_intermediate_file','-d', action='store_true')
args = parser.parse_args()
input_path = args.input_path
output_dir = args.output_dir
read_pb_path = args.read_pb_path


dc = pickle.load(open(read_pb_path,'rb'))
for read in dc :
	pbs=dc[read]
	pb1 = 'PS%d_%d_%d'%(pbs[0][0],pbs[0][-2],pbs[0][-1])
	pb2 = 'PS%d_%d_%d'%(pbs[1][0],pbs[1][-2],pbs[1][-1])
	if pbs[0][0]<pbs[1][0]:
		pbs = (pb1,pb2)
	else:
		pbs = (pb2,pb1)
	dc[read]=pbs


with open(input_path,'r') as f:
	s = f.readlines()

os.system("rm -r %s;mkdir %s"%(output_dir,output_dir))
for line in s:
	read = ast.literal_eval(line)[0]
	if read in dc:
		pbs = 'and'.join(dc[read])
		with open(output_dir+'/'+pbs+'.emb','a+') as f:
			f.write(line)