import os
import random

#Analyze files.
files = []
for name in os.listdir("VirusData"):
	print name
	if ("ShortData" in name):
		continue
	splitted = name.split("output")[1].split(".txt")[0]
	print "Got " +  str(int(splitted))
	files.append(int(splitted))
files.sort()
print "After sort " + str(files) 
cnt = 0
numfile = 1
for fname in files:
	with open("VirusData/output" + str(fname) + ".txt") as file:
		lines = file.readlines()
		print "Number of lines for file " + str(fname) + " is : " + str(len(lines))
		cur_len = int(300 + random.random() * 100)
		num_times = len(lines) / cur_len
		left_over = len(lines) % cur_len
		print "For length of " + str(cur_len) + "number of times is " + str(num_times) + "and left over " + str(left_over)
		for i in range(0,num_times):
			newfile = open("lioroutput" + str(numfile) + ".txt","w+")
			for j in range(0,cur_len):
				#Write line to file.
				newfile.write(lines[i * cur_len + j])
			#Increment number of file.
			newfile.close()	
			numfile += 1

			
