#!/home/narkem/Anaconda3/bin/python


import os
import re
import sys
import erknltk
import erkpoly


inputfile = sys.argv[1]

f = open(inputfile, "r") 

filename = re.findall('.*\/(.*)\.xml', inputfile)[0]

folder = "data/outputs/output_for_" + filename + "/"

if not os.path.exists(folder):
    os.makedirs(folder)

print("File we are working on : " + filename) 

frg = open(folder + "frog-tags_for_" + filename + ".txt", "w+") 

fm = open(folder + "training-tags_for_" + filename + ".txt", "w+")

toksentlist = []

strsentlist = []

tokenlist = []

alltokens = []

frogtl = [] # tl => taglist

trainingtl = []

training = False

firstline = True

for line in f:
	
	dperl = line.split("\t")

	if(firstline):
		firstline = False
		continue

	
	elif(len(dperl) > 2):	

		token = dperl[1]

		if(len(dperl) == 12):

			training = True			

			tag = dperl[9]

			ttag = dperl[2]

			if(ttag == "_"):
				ttag = "O"

			trainingtl.append(ttag)

			#print(token + "," + ttag + "\n")
			fm.write(token + "," + ttag + "\n")

		elif(len(dperl) == 10):

			tag = dperl[7]

			fm.write("There was no training tag.\n")

		else:
			print("Input file format is not compatible")


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


f3 = open(folder + "results_for" + filename + ".txt", "w+")



if(training == False):

	totallist = zip(alltokens, frogtl, nltktl, polytl)

	f3.write("Token , Frog Tag, NLTK Tag, Polyglot Tag\n")
	f3.write("========================================\n")

	for to, fro, nlt, pol in totallist:

		print(to  + "," + fro + "," + nlt + "," + pol)
		f3.write(to  + "," + fro + "," + nlt + "," + pol + "\n")

elif(training == True):
	
	totallist = zip(alltokens, trainingtl, frogtl, nltktl, polytl)

	f3.write("Token, Training Tags, Frog Tag, NLTK Tag, Polyglot Tag\n")
	f3.write("========================================\n")

	for to, tra, fro, nlt, pol in totallist:

		print(to + "," + tra + "," + fro + "," + nlt + "," + pol)
		f3.write(to + "," + tra + "," + fro + "," + nlt + "," + pol + "\n")



f.close()
frg.close()
fm.close()
f3.close()

