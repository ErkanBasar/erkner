#!/home/narkem/Anaconda3/bin/python

import re
import nltk
import pickle
import sys
sys.path.insert(1, r'nltk-trainer/')


def ner(tokenlist):

	with open("data/nltk-training/dutch-tagger.pickle", 'rb') as pickle_file: 
	    tagger = pickle.load(pickle_file)

	with open("data/nltk-training/conll2002_ned_NaiveBayes.pickle", 'rb') as pickle_file:
	    chunker = pickle.load(pickle_file)

	str_tags = tagger.tag(tokenlist)

	str_chunks = chunker.parse(str_tags)
	
	return str_chunks


def lister(toksentlist, filename, folder):

	taglist = []

	f = open(folder + "nltk-tags_for_" + filename + ".txt", "w+") 

	for sent in toksentlist:

		chunks = ner(sent)

		for c in chunks:

			if(type(c) == nltk.tree.Tree):
				
					tag = re.findall('\((PER|MISC|ORG|LOC).*', str(c))[0]

					for index, lv in enumerate(c.leaves()):

						if(len(c.leaves()) == 1):
							
							f.write(lv[0] + "\t"  + "(" + tag + ")" + "\n")

							taglist.append("(" + tag + ")")

						else:
							if(index == 0):

								f.write(lv[0] + "\t"  + "(" + tag + "\n")

								taglist.append("(" + tag)
						
							elif(index == len(c.leaves())-1):

								f.write(lv[0] + "\t"  + tag + ")" + "\n")

								taglist.append(tag + ")")

							else:
					
								f.write(lv[0] + "\t" + tag + "\n")

								taglist.append(tag)

			else:

				f.write(str(c[0]) + "\tO" + "\n")
	
				taglist.append("O")


	f.close()

	return taglist


if __name__ == "__main__":

	str2 = 'Christiane heeft een lam.'

	tokenlist = nltk.word_tokenize(str2)

	lister(tokenlist, "hede", "data/")

	print(ner(tokenlist), "test")

	





