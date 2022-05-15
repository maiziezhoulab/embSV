from argparse import ArgumentParser
import pysam
import pickle
parser = ArgumentParser(description="",usage='use "python3 %(prog)s --help" for more information')
parser.add_argument('--input_path','-i')
parser.add_argument('--output_path','-o')
parser.add_argument('--pb_info','-pb')
parser.add_argument('--delete_intermediate_file','-d', action='store_true')
args = parser.parse_args()
input_path = args.input_path
output_path = args.output_path
pb_info = args.pb_info

dc_info = pickle.load(open(pb_info,'rb'))


samfile = pysam.AlignmentFile(input_path)

dc ={}
for read in samfile.fetch():
	name = read.query_name
	pb = 0
	for tag in read.get_tags():
		if tag[0]=='PS':
			pb = tag[1]
		if tag[0]=='HP':
			hp = tag[1]
	if pb:
		pb_start = dc_info[str(pb)][0]
		pb_end = dc_info[str(pb)][1]
		hp = 'PS%d_%d_%d_hp%d'%(pb,pb_start,pb_end,hp)
		dc[name]=hp

pickle.dump(dc,open(output_path,'wb'))



