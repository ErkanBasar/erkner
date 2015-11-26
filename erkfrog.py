#!/home/narkem/lamachine/bin/python

import frog

fo = frog.FrogOptions()
fr = frog.Frog(fo, "/home/narkem/lamachine/etc/frog/frog.cfg")

def ner(text):

	f = open("tmp-frog.txt", "w+")

	for info in fr.process(text):
		print(info['text'] + ' : ' + info['chunker'] + " , " + info['ner'])

		f.write(info['text'] + ' : ' + info['chunker'] + " , " + info['ner'] + "\n")


	f.close()

if __name__ == "__main__":

	str2 = 'Christiane heeft een lam.'

	print(ner(str2))
