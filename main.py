#!/home/narkem/Anaconda3/bin/python


import re
import os
import sys
import erknltk
import erkpoly


inputfile = sys.argv[1]

print("File we are working on : " + inputfile) 

f = open(inputfile, "r") 

filename = re.findall('.*\/(.*)\.xml', inputfile)[0]

f2 = open("frog-tags_for_" + filename + ".txt", "w+") 

tokenlist = []

frogtl = [] # tl => taglist


for line in f:
	
	dperl = line.split("\t")
	
	if(len(dperl) > 7):	

		#print(dperl[1] + "\t:\t" + dperl[9])
		f2.write(dperl[1] + "\t:\t" + dperl[9] + "\n")
		
		tokenlist.append(dperl[1])	


		frogtl.append(dperl[9])	


text = ' '.join(tokenlist)

f20 = open("text.txt", "w+") 

f20.write(text)

f20.close()

#os.system("/home/narkem/workspaces/EntityRecog/erkfrog.py " + text)


nltktl = erknltk.lister(tokenlist, filename)

polytl = erkpoly.ner(text, tokenlist, filename)


totallist = zip(tokenlist, frogtl, nltktl)


#for to, fro, nlt in totallist:

	#print(to  + "\t:\t" + fro + "\t:\t" + nlt)

	
	



f.close()
f2.close()


