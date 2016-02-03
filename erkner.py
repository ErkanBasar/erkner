#!/home/narkem/Anaconda3/bin/python


import os
import re
import sys
import erknltk
import erkpoly
import erktest

from subprocess import call

from difflib import SequenceMatcher


def similar(a, b):
   return SequenceMatcher(None, a, b).ratio()

inputfile = sys.argv[1]

evaluation = False
if(len(sys.argv) > 2):
	if(sys.argv[2] == "--eval"):
		evaluation = True

f = open(inputfile, "r") 

regex = re.findall('data/inputs/frogged/(.*)\/(.*)', inputfile)[0]
upfolder = regex[0]
filename = os.path.splitext(regex[1])[0]

folder = "data/outputs/" + upfolder +  "/output_for_" + filename + "/"

if not os.path.exists(folder):
    os.makedirs(folder)

print("File we are working on : " + filename) 

frg = open(folder + "frog-tags_for_" + filename + ".txt", "w+") 


toksentlist = [] # tokenized sentences list

strsentlist = [] # string sentences list

tokenlist = [] # tokens per sentence

alltokens = []

frogtl = [] # tl => taglist

linelist = f.readlines()


for i, line in enumerate(linelist):
	
	dperl = line.split("\t")

	if(len(dperl) > 1  and not i == len(linelist)-1):	

		next = linelist[i+1]

		token = dperl[1]

		ftag = dperl[6] # frog tag

		if(not ftag == "O"):

			intag = re.findall(".-(PER|MISC|ORG|LOC|PRO|EVE)", ftag)[0]

			if(re.match("B-(PER|MISC|ORG|LOC|PRO|EVE)", ftag)):

				if(len(next.split("\t")) > 1):

						if(re.match("I-(PER|MISC|ORG|LOC|PRO|EVE)", next.split("\t")[6])):

							ftag = "(" + intag

						else:

							ftag = "(" + intag + ")"

				else:
						ftag = "(" + intag + ")"


			elif(re.match("I-(PER|MISC|ORG|LOC|PRO|EVE)", ftag)):

				if(len(next.split("\t")) > 1):

						if(re.match("I-(PER|MISC|ORG|LOC|PRO|EVE)", next.split("\t")[6])):

							ftag = intag	

						else:

							ftag = intag + ")"

				else:

					ftag = intag + ")"



		frg.write(token + "\t" + ftag + "\n")
		
		tokenlist.append(token)	

		alltokens.append(token)

		frogtl.append(ftag)	


	elif(len(dperl) > 1 and i == len(linelist)-1):

		toksentlist.append(tokenlist)

		sentence = ' '.join(tokenlist)

		strsentlist.append(sentence)

		break

	else:

		toksentlist.append(tokenlist)

		sentence = ' '.join(tokenlist)

		strsentlist.append(sentence)

		tokenlist = []

		continue



texttotal = ' '.join(strsentlist) # Complete text as string. 


print("Frog data done.")


nltktl = erknltk.lister(toksentlist, filename, folder)

print("NLTK done.")


polytl = erkpoly.ner(texttotal, filename, folder)

print("Polyglot done.")


f3 = open(folder + "results_for_" + filename + ".txt", "w+")

ferk = open(folder + "erk-tags_for_" + filename + ".txt", "w+")


resp_folder = "data/outputs/responses/" + upfolder

if not os.path.exists(resp_folder):
    os.makedirs(resp_folder)

ferkclin = open(resp_folder + "/" + filename + ".txt.xml.ne", "w+")


totallist = zip(alltokens, frogtl, nltktl, polytl)

f3.write("# Token, Frog Tag, NLTK Tag, Polyglot Tag, Erk Tag\n")

erk = "" 

ln = 1 # line number

for tok, fro, nlt, pol in totallist:

	if(nlt == fro and nlt == pol and fro == pol):
		erk = fro

	elif(fro == pol and not fro == nlt):
		erk = fro

	elif(nlt == pol and not nlt == fro):
		erk = nlt

	elif(nlt == fro and not nlt == pol):
		erk = fro

	else: #If they are all different, trust frog
		erk = fro


	ferk.write(tok + "\t" + erk + "\n")

	if(erk == "O"):
		ferkclin.write(str(ln) + "\t" + tok + "\t" + "_" + "\t_" + "\n")
	else:
		ferkclin.write(str(ln) + "\t" + tok + "\t" + erk + "\t_" + "\n")

	f3.write(str(ln) + "\t" + tok + "\t" + fro + "\t" + nlt + "\t" + pol + "\t" + erk + "\n")

	ln += 1


f.close()
frg.close()
f3.close()
ferk.close()


print("ERK done.")


if(evaluation == True):

	inputfile = folder + "results_for_" + filename + ".txt"

	call(["./erktest.py", inputfile, "--all"])
	print("ERK Evaluation done.")




