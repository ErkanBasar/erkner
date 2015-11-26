#!/home/narkem/Anaconda3/bin/python

#from polyglot.text import Text, Sentence

#from difflib import SequenceMatcher

import os
import re
from subprocess import call


def ner(text, filename):

	ft = open("tmptext.txt", "w+")
	ft.write(text)
	ft.close()

	f1 = open("poly-tags_for_" + filename + ".txt", "w+")
	#polyglot --lang nl ner --input text.txt > poly.txt;
	call(["polyglot", "--lang", "nl", "ner", "--input", "tmptext.txt"], stdout=f1)
	f1.close()

	os.remove("tmptext.txt")

	polytl = []

	tokenlist = []

	f2 = open("poly-tags_for_" + filename + ".txt", "r+")

	lines = f2.readlines()

	for line in lines[:-1]:

		tag = re.findall('(\w+|.)\s*(O|I-PER|I-ORG|I-LOC).*', line)[0]

		#print(tag[0] + "\t:\t" + tag[1])
		
		tokenlist.append(tag[0])	

		polytl.append(tag[1])	


	f2.close()


	return polytl




#def ner(strsentlist, toksentlist, filename):

#	f = open("poly-tags_for_" + filename + ".txt", "w+") 

#	print(strsentlist)

#	texttotal = ' '.join(strsentlist)

#	text = Text(texttotal)

#	for sent in text.sentences:

#		print("-------------------\n", sent)
#		f.write("------------------\n")

#		entitylist = sent.entities

#		for entity in entitylist:			

#			print(entity[0] + " : " + entity.tag)
#			f.write(entity[0] + " : " + entity.tag + "\n")


#	f.close()

#	return 0


#def similar(a, b):
#   return SequenceMatcher(None, a, b).ratio()


#if __name__ == "__main__":


#	str2 = ['Christiane heeft een lam.']

#	print(ner(str2, "ner"))


