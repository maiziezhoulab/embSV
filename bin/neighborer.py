#import fasttext
#import scipy
#import scipy.spatial
import ast
import numpy as np
#from sklearn.manifold import TSNE
from MulticoreTSNE import MulticoreTSNE as TSNE
import matplotlib.pyplot as plt
import sys

dir = "/data/maiziezhou_lab/Parth/long_reads_project/"
# filenum = 5
# kmerlength = 120
# unphasedlines = 185
# alllines = 1797
blocks = [[0, 204], [204, 436], [436, 1284], [1284, 1612], [1612, 1797]]

def extractBlocks(input):
	s = input.split(",")
	return [[int(s[i]), int(s[i+1])] for i in range(len(s)-1)]

def resetFiles(input):
	for r in input:
		r.seek(0, 0)

def findBlock(num):
	lst = [(num < x[1] and num >= x[0]) for x in blocks]
	return lst.index(True)

embedfilepath = dir + "pipeline/embeds.emb"
logfilepath = dir + "pipeline/nearestNeighbors.txt"
figurepath = dir + "pipeline/TSNECluster.pdf"
#Read in alternative
if(len(sys.argv) > 1):
	# dir = sys.argv[1]
	embedfilepath = sys.argv[1]
	logfilepath = sys.argv[2]
	blocks = extractBlocks(sys.argv[3])


with open(embedfilepath.replace("embeds.emb","blocks.txt"),'w') as f:
	f.write(sys.argv[3])

if (len(sys.argv) > 4):
	figurepath = sys.argv[4]

tsne_path = logfilepath.replace("nearestNeighbors.txt",'TSNE_cords.txt')
embedfile = open(embedfilepath, "r")
logfile = open(logfilepath, "w")
tsnefile = open(tsne_path,'w')

names = [[], [], [], [], []]
for count, line in enumerate(embedfile):
	b = findBlock(count)
	names[b].append(ast.literal_eval(line))
	names[b][-1][1] = np.array(names[b][-1][1])

newnames = []
for b in names:
    for count, val in enumerate(b):
        newnames.append(b[count][1])
        # newnames[-1] = [float(x) for x in newnames[-1]]

Y = TSNE(n_components=2,init='random',random_state=10).fit_transform(np.array(newnames))

Ystr = Y.astype(str)
# print(Ystr)
Yline = []
for i in range(len(Ystr)):

	line = list(Ystr[i])

	Yline.append(','.join(line)+'\n')
	
# print(Ystr)
tsnefile.writelines(Yline)
tsnefile.close()
if (len(sys.argv) > 4):
	plt.scatter(Y[blocks[0][0]:blocks[0][1]][:,0],Y[blocks[0][0]:blocks[0][1]][:,1],alpha=1,s=1, color="blue")
	plt.scatter(Y[blocks[1][0]:blocks[1][1]][:,0],Y[blocks[1][0]:blocks[1][1]][:,1],alpha=1,s=1, color="black")
	plt.scatter(Y[blocks[2][0]:blocks[2][1]][:,0],Y[blocks[2][0]:blocks[2][1]][:,1],alpha=1,s=1, color="green")
	plt.scatter(Y[blocks[3][0]:blocks[3][1]][:,0],Y[blocks[3][0]:blocks[3][1]][:,1],alpha=1,s=1, color="red")
	plt.scatter(Y[blocks[4][0]:blocks[4][1]][:,0],Y[blocks[4][0]:blocks[4][1]][:,1],alpha=0.5,s=1, color="purple")
	plt.legend(['Block 1 Hap 1','Block 1 Hap 2', 'Block 2 Hap 1', 'Block 2 Hap 2', 'Unphased'], loc='upper left', 
	bbox_to_anchor=(1,0.5))
	plt.savefig(figurepath, bbox_inches="tight")

for offset, name in enumerate(names[-1]):
	neis = [[], [], [], []]
	for count, b in enumerate(names[:-1]):
		for otheroffset, n in enumerate(b):
			# cosine_similarity = 1 - scipy.spatial.distance.cosine(Y[blocks[-1][0] + offset], Y[blocks[count][0] + otheroffset])
			distance = np.linalg.norm(Y[blocks[-1][0] + offset] - Y[blocks[count][0] + otheroffset], ord=2)
			neis[count].append([distance, n[0]])
		neis[count].sort()
		neis[count] = neis[count][0:20]
	
	logfile.write(name[0] + "\n")
	for i in range(2):
		for j in range(2):
			logfile.write("Phase Block " + str(i+1) + " Hap " + str(j+1) +":\n")
			neis[2*i+j] = [(l[1] + ", " + str(l[0])) for l in neis[2*i+j]]
			logfile.write('\n'.join(neis[2*i+j]) + "\n\n")

logfile.close()
embedfile.close()
