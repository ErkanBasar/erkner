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

	for line in lines[:-1]:

		tag = re.findall('(\w+|.)\s*(O|I-PER|I-ORG|I-LOC).*', line)[0]

		if(not tag[1] == "O"):
			tag1 = re.findall('I-(PER|ORG|LOC)', tag[1])[0]
		else:
			tag1 = tag[1]		

		f3.write(tag[0] + "\t" + tag1 + "\n")
		
		tokenlist.append(tag[0])	

		polytl.append(tag1)	


	f2.close()
	os.remove(".polytmp.txt")

	f3.close()


	return polytl



#from polyglot.text import Text, Sentence
#from difflib import SequenceMatcher
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
