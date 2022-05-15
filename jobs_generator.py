import os
global code_dir
code_dir=os.path.dirname(os.path.realpath(__file__))+'/bin/'

with open("./input.config",'r') as f:
	config = f.readlines()
input_bam=config[0].split()[1]
file_prefix=config[1].split()[1]
chr_num=config[2].split()[1]
output_dir=config[3].split()[1]
ref_genome=config[4].split()[1]
num_bucket=config[5].split()[1]
kmer_size=config[6].split()[1]
dim=config[7].split()[1]


# with open("bin/all_steps/DipPAV_step1.sh",'r') as f:
# 	s1= f.read()
# with open("bin/all_steps/DipPAV_step2.sh",'r') as f:
# 	s2= f.read()
# with open("bin/all_steps/DipPAV_step3.sh",'r') as f:
# 	s3= f.read()
# with open("bin/all_steps/DipPAV_step4.sh",'r') as f:
# 	s4= f.read()
# with open("bin/all_steps/DipPAV_step5.sh",'r') as f:
# 	s5= f.read()


# s1_new = s1.replace("<code_dir>",code_dir)\
# .replace("<input_bam>",input_bam)\
# .replace("<file_prefix>",file_prefix)\
# .replace("<chr_num>",chr_num)\
# .replace("<output_dir>",output_dir)\
# .replace("<ref_genome>",ref_genome)\
# .replace("<num_bucket>",num_bucket)\
# .replace("<kmer_size>",kmer_size)\
# .replace("<dim>",dim)

def script_gen(input_path,output_path):
	with open(input_path,'r') as f:
		s= f.read()
	s_new = s.replace("<code_dir>",code_dir)\
.replace("<input_bam>",input_bam)\
.replace("<file_prefix>",file_prefix)\
.replace("<chr_num>",chr_num)\
.replace("<output_dir>",output_dir)\
.replace("<ref_genome>",ref_genome)\
.replace("<num_bucket>",num_bucket)\
.replace("<kmer_size>",kmer_size)\
.replace("<dim>",dim)
	with open(output_path,'w') as f:
		f.write(s_new)


script_gen("bin/all_steps/DipPAV_step1.sh","./DipPAV_step1.sh")
script_gen("bin/all_steps/DipPAV_step2.sh","./DipPAV_step2.sh")
script_gen("bin/all_steps/DipPAV_step3.sh","./DipPAV_step3.sh")
script_gen("bin/all_steps/DipPAV_step4.sh","./DipPAV_step4.sh")
script_gen("bin/all_steps/DipPAV_step5.sh","./DipPAV_step5.sh")












