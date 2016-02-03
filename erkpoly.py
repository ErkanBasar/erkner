#!/home/narkem/Anaconda3/bin/python


import os
import re
from subprocess import call


def ner(text, filename, folder):

	ft = open(".tmptext.txt", "w+")
	ft.write(text)
	ft.close()

	f1 = open(".polytmp.txt", "w+")
	#polyglot --lang nl ner --input text.txt > poly.txt;
	call(["polyglot", "--lang", "nl", "ner", "--input", ".tmptext.txt"], stdout=f1)
	f1.close()

	os.remove(".tmptext.txt")
	f1.close()

	polytl = []

	tokenlist = []

	f2 = open(".polytmp.txt", "r+")
	f3 = open(folder + "poly-tags_for_" + filename + ".txt", "w+")

	lines = f2.readlines()

	for i, line in enumerate(lines):

		if(i == len(lines)-1):
			break

		regex = re.findall('(\w+|.)\s*(O|I-PER|I-ORG|I-LOC).*', line)[0]
		token = regex[0]
		tag = regex[1]

		if(not tag == "O"):

			intag = re.findall('I-(PER|ORG|LOC)', tag)[0]

			next = lines[i+1]
			regex = re.findall('(\w+|.)\s*(O|I-PER|I-ORG|I-LOC).*', next)[0]
			nexttag = regex[1]

			if(not i == 0):

				prev = lines[i-1]
				regex = re.findall('(\w+|.)\s*(O|I-PER|I-ORG|I-LOC).*', prev)[0]
				prevtag = regex[1]

				if(not nexttag == tag and not prevtag == tag):
	
					tag = "(" + intag + ")"

				elif(not nexttag == tag and prevtag == tag):

					tag = intag + ")"

				elif(nexttag == tag and not prevtag == tag):

					tag = "(" + intag

				elif(nexttag == tag and prevtag == tag):

					tag = intag

			else:

				if(not nexttag == tag):
	
					tag = "(" + intag + ")"

				else:

					tag = "(" + intag


		f3.write(token + "\t" + tag + "\n")
		
		tokenlist.append(token)	

		polytl.append(tag)	


	f2.close()
	os.remove(".polytmp.txt")

	f3.close()


	return polytl



