#!/home/narkem/lamachine/bin/python

import os
import re
import sys
from subprocess import call

inputfile = sys.argv[1]

f = open(inputfile, "r") 

regex = re.findall('data/inputs/(.*)\/(.*)\.xml', inputfile)[0]
upfolder = regex[0]
filename = os.path.splitext(regex[1])[0]

print("File we are working on : " + filename) 

lt = open(".sentencestmp.txt", "w+") 

tokenlist = [] # tokenlist (sentence tokens)

for line in f:
	
	dperl = line.split("\t")
	
	if(len(dperl) > 1):	

		token = dperl[1]
		
		tokenlist.append(token)	

	else:

		sentence = ' '.join(tokenlist)

		lt.write(sentence + "\n\n")

		tokenlist = []

		continue

lt.close()


folder = "data/inputs/frogged/" + upfolder + "/" 

if not os.path.exists(folder):
    os.makedirs(folder)

outputfile = folder + filename + ".txt"


call(["frog", "-t", ".sentencestmp.txt", "--skip=[mpt]", "-o", outputfile])


os.remove(".sentencestmp.txt")








