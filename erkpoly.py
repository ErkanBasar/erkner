#!/home/narkem/Anaconda3/bin/python

from polyglot.text import Text


def ner(text, tokenlist, filename):

	f = open("poly-tags_for_" + filename + ".txt", "w+") 


	text = Text(text)

	print(text.entities)

	#for entity in nertree:
	
	 #   print(entity.tag, entity)


	for sent in text.sentences:

		  #print(sent, "\n")

		for entity in sent.entities:

				print(entity.tag, entity)
				print(entity, text.words[entity.start: entity.end])

	f.close()

	return 0



#	i = 0
#	for i in range(len(tokens)): # enumerate(tokens):
#		if(i == len(tokens)-1):
#			print(tokens[i])
#			f.write(tokens[i] + "\n")			
#			break
#		elif(tokens[i - 1] == "-"):
#			continue
#		elif(tokens[i + 1] == "-"):
#			if(tokens[i + 3] == "-"):
#				print(tokens[i] + tokens[i + 1] + tokens[i + 2] + tokens[i + 3] + tokens[i + 4])
#				f.write(tokens[i] + tokens[i + 1] + tokens[i + 2] + tokens[i + 3] + tokens[i + 4] + "\n")
#			else:
#				print(tokens[i] + tokens[i + 1] + tokens[i + 2])
#				f.write(tokens[i] + tokens[i + 1] + tokens[i + 2] + "\n")
#		elif(tokens[i] == "-"):
#			continue
#		else:
#			print(tokens[i])
#			f.write(tokens[i] + "\n")


if __name__ == "__main__":

	str2 = 'Christiane heeft een lam.'

	print(ner(str2, "ner"))
