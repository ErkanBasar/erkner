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

fm = open(folder + "training-tags_for_" + filename + ".txt", "w+")

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

			tag = dperl[9]

			ttag = dperl[2]

			if(ttag == "_"):
				ttag = "O"

		elif(len(dperl) == 10):

			tag = dperl[7]

			ttag = "O"

		else:
			print("Input file format is not compatible")


		trainingtl.append(ttag)

		fm.write(token + "," + ttag + "\n")

		frg.write(token + "," + tag + "\n")
		
		tokenlist.append(token)	

		alltokens.append(token)

		frogtl.append(tag)	


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



f3 = open(folder + "results_for_" + filename + ".txt", "w+")


totallist = zip(alltokens, trainingtl, frogtl, nltktl, polytl)

f3.write("# Token, Training Tags, Frog Tag, NLTK Tag, Polyglot Tag, Erk Tag\n")

erk = ""

ln = 0 # line number

for tok, tra, fro, nlt, pol in totallist:

	if(nlt == fro and nlt == pol and fro == pol):
		erk = nlt

	elif(similar(fro,nlt) >= 0.8 or similar(fro,pol) >= 0.8):
		erk = fro

	elif(similar(nlt,pol) >= 0.8):
		erk = nlt

	else:
		erk=nlt

	print(str(ln) + "\t" + tok + "\t" + tra + "\t" + fro + "\t" + nlt + "\t" + pol + "\t" + erk)
	f3.write(str(ln) + "\t" + tok + "\t" + tra + "\t" + fro + "\t" + nlt + "\t" + pol + "\t" + erk + "\n")

	ln += 1






f.close()
frg.close()
fm.close()
f3.close()


