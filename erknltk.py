#!/home/narkem/Anaconda3/bin/python

import re
import nltk
import pickle
import sys
sys.path.insert(1, r'nltk-trainer/')


def ner(tokenlist):

	with open("nltk-trainingdata/dutch-tagger.pickle", 'rb') as pickle_file: 
	    tagger = pickle.load(pickle_file)

	with open("nltk-trainingdata/conll2002_ned_NaiveBayes.pickle", 'rb') as pickle_file:
	    chunker = pickle.load(pickle_file)

	str_tags = tagger.tag(tokenlist)

	str_chunks = chunker.parse(str_tags)
	
	return str_chunks


def lister(tokenlist, filename):

	taglist = []

	chunks = ner(tokenlist)

	#print(chunks)

	f = open("nltk-tags_for_" + filename + ".txt", "w+") 

	for c in chunks:

		if(type(c) == nltk.tree.Tree):
				
				tag = re.findall('\((PER|MISC|ORG|LOC).*', str(c))

				for index, lv in enumerate(c.leaves()):

					if(index == 0):

						#print(lv[0] + "\t:\t" + "B-" +  tag[0])
						f.write(lv[0] + "\t:\t" + "B-" + tag[0] + "\n")

						taglist.append("B-" + tag[0])

					else:
					
						#print(lv[0] + "\t:\t"  + "I-" + tag[0])
						f.write(lv[0] + "\t:\t"  + "I-" + tag[0] + "\n")

						taglist.append("I-" + tag[0])

		else:
			#print(c[0])
			f.write(str(c[0]) + "\t:\t0" + "\n")

			taglist.append(c[0])


	f.close()

	return taglist


if __name__ == "__main__":

	str2 = 'Christiane heeft een lam.'

	tokenlist = nltk.word_tokenize(str2)

	print(ner(tokenlist), "test")

	





