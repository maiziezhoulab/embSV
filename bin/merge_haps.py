from argparse import ArgumentParser
import os
from subprocess import Popen
parser = ArgumentParser(description="",usage='use "python3 %(prog)s --help" for more information')
parser.add_argument('--input_dir1','-d1')
parser.add_argument('--input_dir2','-d2')
parser.add_argument('--output_dir','-o')
parser.add_argument('--delete_intermediate_file','-d', action='store_true')
args = parser.parse_args()
input_dir1 = args.input_dir1
input_dir2 = args.input_dir2
output_dir = args.output_dir
os.system("rm -r "+output_dir)
os.system("mkdir "+output_dir)
all_hps1 = sorted(os.listdir(input_dir1))
all_hps2 = sorted(os.listdir(input_dir2))

all_hp = list(set(all_hps1)|set(all_hps2))

with open(output_dir+'/num.log','w') as f:
	f.write('\n'.join(all_hp)+'\n')

for hp in all_hp:
	if hp in all_hps1 and hp in all_hps2:
		cmd = "cat %s/%s %s/%s > %s/%s"%(input_dir1,hp,input_dir2,hp,output_dir,hp)
		Popen(cmd,shell=True).wait()
	elif hp in all_hps1 and hp not in all_hps2:
		cmd = "cp %s/%s  %s/%s"%(input_dir1,hp,output_dir,hp)
		Popen(cmd,shell=True).wait()
	elif hp not in all_hps1 and hp in all_hps2:
		cmd = "cp %s/%s  %s/%s"%(input_dir2,hp,output_dir,hp)
		Popen(cmd,shell=True).wait()



