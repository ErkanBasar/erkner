#!/home/narkem/Anaconda3/bin/python


import os
import re
import sys

from difflib import SequenceMatcher


def similar(a, b):
   return SequenceMatcher(None, a, b).ratio()



def evaluation(systag1, systag2, filename, folder, inputfile):

	f = open(inputfile, "r")

	folder2 = folder + "evaluations_for_" + filename + "/"

	if not os.path.exists(folder2):
		os.makedirs(folder2)

	fout = open(folder2 + systag1 + "_" + systag2  + "_" + filename + ".txt", "w+") 

	ln = 0 #line number

	corm = 0
	miss = 0
	wrom = 0
	wroc = 0

	precision = 0
	recall = 0

	#print("\n############################\n# " + systag1.upper() + " & " + systag2.upper() + " EVALUATION\n############################")

	#print("\nLN\tStatus\t" + systag1.upper() + "\t" + systag2.upper() + "\tToken"  
	#  + "\n==========================================")

	fout.write("LN\tStatus\t" + systag1.upper() + "\t\t" + systag2.upper() + "\t\tToken"  
	  + "\n==========================================\n")


	firstline = True

	for line in f:

		if(firstline):
			firstline = False
			continue

		dperl = line.split("\t")

		token = dperl[1]
		tra = dperl[2] # training tag
		fro = dperl[3] # frog tag
		nlt = dperl[4] # nltk tag
		pol = dperl[5] # polyglot tag
		erk = dperl[6].rstrip('\n') # result from erkner tag


		if(systag1 == "tra"):
			tag1 = tra

		elif(systag1 == "fro"):
			tag1 = fro

		elif(systag1 == "nlt"):
			tag1 = nlt

		elif(systag1 == "pol"):
			tag1 = pol

		elif(systag1 == "erk"):
			tag1 = erk


		if(systag2 == "tra"):
			tag2 = tra

		elif(systag2 == "fro"):
			tag2 = fro

		elif(systag2 == "nlt"):
			tag2 = nlt

		elif(systag2 == "pol"):
			tag2 = pol

		elif(systag2 == "erk"):
			tag2 = erk


		if(similar(tag1, tag2) >= 0.3 and not tag1 == "O"):
			#print(str(ln) + "\tCorM :\t" + tag1 + "\t" + tag2 + "\t " + token)
			fout.write(str(ln) + "\tCorM :\t" + tag1 + "\t\t"+ tag2 + "\t " + token + "\n")
			corm += 1

		elif(tag1 == "O" and not tag2 == "O"):
			#print(str(ln) + "\tMiss :\t" + tag1 + "\t" + tag2 + "\t " + token)
			fout.write(str(ln) + "\tMiss :\t" + tag1 + "\t\t" + tag2 + "\t " + token + "\n")
			miss += 1

		elif(not tag1 == "O" and tag2 == "O"):
			#print(str(ln) + "\tWroC :\t" + tag1 + "\t"+ tag2 + "\t " + token)
			fout.write(str(ln) + "\tWroC :\t"+ tag1 + "\t\t"+ tag2 + "\t\t" + token + "\n")
			wroc += 1

		elif(similar(tag1, tag2) < 0.3 and not tag1 == "O" and not tag2 == "O"):
			#print(str(ln) + "\tWroM :\t" + tag1 + "\t" + tag2 + "\t " + token)
			fout.write(str(ln) + "\tWroM :\t" + tag1 + "\t\t" + tag2 + "\t " + token  + "\n")
			wrom += 1

		ln += 1


	precision = format(corm/(corm+wrom+wroc), '.2f')

	recall = format(corm/(miss+wrom+corm), '.2f')

#	print("\n\n# "		
#			+ "Evaluation for " + systag1 + " & " + systag2 
#			+ "\n============================\n"
#			+ "Correct Match (CorM) = " + str(corm) + "\n"
#			+ "Wrong Match (WroM) = " + str(wrom) + "\n"
#			+ "Missed (Miss) = " + str(miss) + "\n"
#			+ "Wrong Call (WroC) = " + str(wroc) + "\n"
#			+ "Precision = " + str(precision) + "\n"
#			+ "Recall = " + str(recall))

	fout.write("\n\n# "  
			+ "Evaluation for " + systag1 + " & " + systag2 
			+ "\n============================\n"
			+ "Correct Match (CorM) = " + str(corm) + "\n"
			+ "Wrong Match (WroM) = " + str(wrom) + "\n"
			+ "Missed (Miss) = " + str(miss) + "\n"
			+ "Wrong Call (WroC) = " + str(wroc) + "\n"
			+ "Precision = " + str(precision) + "\n"
			+ "Recall = " + str(recall))
	

	return corm, wrom, miss, wroc, precision, recall


	f.close()
	fout.close()



def writte(systag1, corm, wrom, miss, wroc, precision, recall):

	fevas = open(folder2 + "evaluations_for_" + filename + ".txt", "a")

	fevas.write("\n\n# "  
			+ "Evaluation for " + systag1 
			+ "\n============================\n"
			+ "Correct Match = " + str(corm) + "\n"
			+ "Wrong Match = " + str(wrom) + "\n"
			+ "Missed = " + str(miss) + "\n"
			+ "Wrong Call = " + str(wroc) + "\n"
			+ "Precision = " + str(precision) + "\n"
			+ "Recall = " + str(recall))



if __name__ == "__main__":

	inputfile = sys.argv[1]

	filename = re.findall('.*\/results_for_(.*)\.txt', inputfile)[0]

	folder = "data/outputs/output_for_" + filename + "/"

	folder2 = folder + "evaluations_for_" + filename + "/"

	if not os.path.exists(folder2):
		os.makedirs(folder2)

	#print("File we are working on : " + filename) 


	if(len(sys.argv) > 2 and sys.argv[2] == "--all"):

		fevas = open(folder2 + "evaluations_for_" + filename + ".txt", "w+")

		fc, fw, fm, fwc, fp, fr = evaluation("fro", "tra", filename, folder, inputfile)
		nc, nw, nm, nwc, np, nr = evaluation("nlt", "tra", filename, folder, inputfile)
		pc, pw, pm, pwc, pp, pr = evaluation("pol", "tra", filename, folder, inputfile)
		ec, ew, em, ewc, ep, er = evaluation("erk", "tra", filename, folder, inputfile)

		writte("Frog", fc, fw, fm, fwc, fp, fr)
		writte("NLTK", nc, nw, nm, nwc, np, nr)
		writte("Polyglot", pc, pw, pm, pwc, pp, pr)
		writte("ERK", ec, ew, em, ewc, ep, er)
		
		fevas.close()


	else:

		systag1 = input('Tag1 (tra, fro, nlt, pol, erk) : ') or "erk"
		systag2 = input('Tag2 (tra, fro, nlt, pol, erk) : ') or "tra"

		evaluation(systag1, systag2, filename, folder, inputfile)










