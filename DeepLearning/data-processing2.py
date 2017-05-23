import os
import collections
import numpy as np


def get_syscalls(folder_name):
    counter = collections.Counter()
    arr = []
    with open("straceSamplesPos/test1/output3.txt") as f:
        lines = f.readlines()
        for line in lines:
            parts = line.split("(")
            parts = parts[0].split(" ")
            arr.append(parts[2])
    counter.update(arr)
    with open("syscalls.txt", "w") as f:
        for key in counter.keys():
            f.write(key + "\n")


def create_sysc2index():
    arr = []
    with open("syscalls.txt", "r") as f:
        lines = f.readlines()
    for line in lines:
        arr.append(line.strip("\n"))
    return {f: i for i, f in enumerate(arr)}  # syscall to indexes dictionary


def create_data(d_sysc2index, data_type):
    new_data = []
    for subfolder in os.listdir('straceSamples' + data_type):
        samples = []
        for fname in os.listdir('straceSamples' + data_type + "/" + subfolder):
            with open("straceSamples" + data_type + "/" + subfolder + "/" + fname) as f:
                lines = f.readlines()
                arr = []
                for line in lines:
                    parts = line.split("(")
                    parts = parts[0].split(" ")
                    arr.append(parts[2])
            # print fname
            # print arr
            counter = collections.Counter()
            counter.update(arr)
            cur = np.zeros((54))
            # print counter
            for elem in counter.keys():
                cur[d_sysc2index.get(elem)] = counter.get(elem)
            # print cur
            samples.append(cur)
        new_data.append(samples)
    return new_data

def create_datav2(d_sysc2index, data_type):
	new_data = []
	for fname in os.listdir('straceSamples' + data_type):
        samples = []
        with open("straceSamples" + data_type  + "/" + fname) as f:
        	lines = f.readlines()
        	while True:
                arr = []
            	for line in lines:
                	parts = line.split("(")
                	parts = parts[0].split(" ")
                	arr.append(parts[2])
            	counter = collections.Counter()
            	counter.update(arr)
            	cur = np.zeros((54))
                for elem in counter.keys():
            	   cur[d_sysc2index.get(elem)] = counter.get(elem)
                samples.append(cur)
        new_data.append(samples)
	return new_data

def zeros_array(size):
    arrr = []
    for i in range(size):
        arrr.append(0)
    return arrr


def save_data(folder_name, my_data):
    for i in range(len(my_data)):
        if not os.path.exists("train/" + folder_name + "/sample" + str(i + 1)):
            os.makedirs("train/" + folder_name + "/sample" + str(i + 1))
        for j in range(10):
            try:
                with open("train/" + folder_name + "/sample" + str(i + 1) + '/vec' + str(j + 1) + '.txt', 'w') as f:
                    np.savetxt(f, my_data[i][j], fmt='%1.0f')
            except:
                print "error"
                raise
                # pass


sysc2index = create_sysc2index()
data = create_data(sysc2index, "Pos")
save_data("Pos", data)