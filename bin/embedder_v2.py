import fasttext
from argparse import ArgumentParser
from tqdm import tqdm
from time import sleep
import numpy as np
parser = ArgumentParser(description="",usage='use "python3 %(prog)s --help" for more information')
parser.add_argument('--model_path','-mod')
parser.add_argument('--hash_path','-hash')
parser.add_argument('--read_name_path','-name')
parser.add_argument('--output_path','-o')
args = parser.parse_args()
model_path = args.model_path
hash_path = args.hash_path
read_name_path = args.read_name_path
output_path = args.output_path
if(".bin" not in model_path):
	model_path += ".bin"


# Load model
print("Loading model...")
model = fasttext.load_model(model_path)

# Find names
print("Loading read names...")
with open(read_name_path) as f:
	names = f.read().split('\n')[:-1]

# Load hash
print("Loading hash...")
with open(hash_path, "r") as f:
	hash_lines = f.readlines()

# Extract embedding
print("Extract embedding...")
emb_list = []
for i in tqdm(range(len(hash_lines)), desc ="Progress:  "):
	emb = model.get_sentence_vector(hash_lines[i].strip())
	emb_list.append([names[i],list(emb)])
	
# Reformatting
print("Reformatting data...")
# emb_list = np.array(emb_list)
# emb_str_list = []
# for i in range(len(emb_list)):
# 	emb_str_list.append(','.join(emb_list[i])+'\n')

# Write output
print("Write embedding...")
with open(output_path,'w') as f:
	for line in emb_list:
		print(line, file=f)
	# f.writelines(emb_str_list)








