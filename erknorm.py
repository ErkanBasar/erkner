#!/home/narkem/Anaconda3/bin/python


import os
import re
import sys

respfile = sys.argv[1]

regex = re.findall('data/outputs/responses/(.*)\/(.*)', respfile)[0]
upfolder = regex[0]
filename = regex[1]

orjfile = "data/inputs/" + upfolder + "/" + filename

fc = open(orjfile, "r")
fr = open(respfile, "r")

cllines = fc.readlines()
relines = fr.readlines()


for i, line in enumerate(cllines):

	if(line == "\n"):

		relines.insert(i, "\n")


fw = open(respfile, "w+")


for line in relines[:-1]:

	fw.write(line)












