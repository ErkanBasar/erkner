#!/home/narkem/Anaconda3/bin/python


import re
import sys
import erknltk
import erkpoly


inputfile = sys.argv[1]

f = open(inputfile, "r") 

filename = re.findall('.*\/(.*)\.xml', inputfile)[0]

print("File we are working on : " + filename) 

f2 = open("frog-tags_for_" + filename + ".txt", "w+") 

toksentlist = []

strsentlist = []

tokenlist = []

alltokens = []

frogtl = [] # tl => taglist


firstline = True

for line in f:
	
	dperl = line.split("\t")

	if(firstline):
		firstline = False
		continue

	
	elif(len(dperl) > 2):	

		#print(dperl[1] + "\t:\t" + dperl[9])
		f2.write(dperl[1] + "\t:\t" + dperl[9] + "\n")
		
		tokenlist.append(dperl[1])	

		alltokens.append(dperl[1])

		frogtl.append(dperl[9])	


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


nltktl = erknltk.lister(toksentlist, filename)

print("NLTK done.")


polytl = erkpoly.ner(texttotal, filename)

print("Polyglot done.")


totallist = zip(alltokens, frogtl, nltktl, polytl)


f3 = open("results_for" + filename + ".txt", "w+")

f3.write("Token , Frog Tag, NLTK Tag, Polyglot Tag\n")
f3.write("========================================\n")

for to, fro, nlt, pol in totallist:

	print(to  + " , " + fro + ", " + nlt + ", " + pol)
	f3.write(to  + " , " + fro + ", " + nlt + ", " + pol + "\n")
	
	



f.close()
f2.close()
f3.close()

