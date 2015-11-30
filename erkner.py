#!/home/narkem/Anaconda3/bin/python


import os
import re
import sys
import erknltk
import erkpoly
import erktest

from difflib import SequenceMatcher


def similar(a, b):
   return SequenceMatcher(None, a, b).ratio()


inputfile = sys.argv[1]

f = open(inputfile, "r") 

filename = re.findall('.*\/(.*)\.xml', inputfile)[0]

folder = "data/outputs/output_for_" + filename + "/"

if not os.path.exists(folder):
    os.makedirs(folder)

print("File we are working on : " + filename) 

frg = open(folder + "frog-tags_for_" + filename + ".txt", "w+") 

ftra = open(folder + "training-tags_for_" + filename + ".txt", "w+")

toksentlist = [] # tokenized sentences list

strsentlist = [] # string sentences list

tokenlist = [] # tokenlist (sentence tokens)

alltokens = []

frogtl = [] # tl => taglist

trainingtl = []

firstline = True

for line in f:
	
	dperl = line.split("\t")

	if(firstline):
		firstline = False
		continue

	
	elif(len(dperl) > 2):	

		token = dperl[1]

		if(len(dperl) == 12):

			if(not dperl[9] == "O"):
				ftag = re.findall(".-(PER|MISC|ORG|LOC|PRO|EVE)", dperl[9])[0]
			else:
				ftag = dperl[9] # frog tag


			ttag = dperl[2] # training tag

			if(ttag == "_"):
				ttag = "O"

		elif(len(dperl) == 10):

			if(not dperl[7] == "O"):
				ftag = re.findall(".-(PER|MISC|ORG|LOC|PRO|EVE)", dperl[7])[0]
			else:
				ftag = dperl[7]

			ttag = "O"

		else:
			print("Input file format is not compatible")


		trainingtl.append(ttag)

		ftra.write(token + "\t" + ttag + "\n")

		frg.write(token + "\t" + ftag + "\n")
		
		tokenlist.append(token)	

		alltokens.append(token)

		frogtl.append(ftag)	


	else:

		toksentlist.append(tokenlist)

		sentence = ' '.join(tokenlist)

		strsentlist.append(sentence)

		tokenlist = []

		continue


else: #belongs to for-loop, the end of the file

	toksentlist.append(tokenlist)

	sentence = ' '.join(tokenlist)

	strsentlist.append(sentence)



texttotal = ' '.join(strsentlist)


print("Frog data done.")


nltktl = erknltk.lister(toksentlist, filename, folder)

print("NLTK done.")


polytl = erkpoly.ner(texttotal, filename, folder)

print("Polyglot done.")


result_file = folder + "results_for_" + filename + ".txt"

f3 = open(result_file, "w+")


totallist = zip(alltokens, trainingtl, frogtl, nltktl, polytl)

f3.write("# Token, Training Tags, Frog Tag, NLTK Tag, Polyglot Tag, Erk Tag\n")
print("# Token, Training Tags, Frog Tag, NLTK Tag, Polyglot Tag, Erk Tag")

erk = ""

ln = 0 # line number

for tok, tra, fro, nlt, pol in totallist:

	if(nlt == fro and nlt == pol and fro == pol):
		erk = nlt

	elif(fro == pol and not fro == nlt):
		erk = fro

	elif(nlt == pol and not nlt == fro):
		erk = nlt 

	elif(nlt == fro and not nlt == pol):
		erk = nlt

	else: #If they are all different, trust nltk
		erk=nlt

	print(str(ln) + "\t" + tok + "\t" + tra + "\t" + fro + "\t" + nlt + "\t" + pol + "\t" + erk)
	f3.write(str(ln) + "\t" + tok + "\t" + tra + "\t" + fro + "\t" + nlt + "\t" + pol + "\t" + erk + "\n")

	ln += 1



#erktest.evaluation("fro", "tra", filename, folder, result_file)
#erktest.evaluation("nlt", "tra", filename, folder, result_file)
#erktest.evaluation("pol", "tra", filename, folder, result_file)
#erktest.evaluation("erk", "tra", filename, folder, result_file)




f.close()
frg.close()
ftra.close()
f3.close()


