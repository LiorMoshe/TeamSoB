from dynet import *
import numpy as np
import random
import os
import collections


def get_syscalls():
    counter = collections.Counter()
    arr = []
    cur_sys = []
    with open("syscalls.txt", "r") as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip('\n')
            cur_sys.append(line)
        counter.update(cur_sys)
    with open("train/straceSamplesPos/output439.txt") as f:
        lines = f.readlines()
        for line in lines:
            if line == "\n":
                pass
            parts = line.split("(")
            parts = parts[0].split(" ")
            try:
                arr.append(parts[3])
            except:
                arr.append(parts[2])
                # print parts, "hereeeeeeeee"
    counter.update(arr)
    print len(counter)
    # print len(counter)
    with open("syscalls.txt", "w") as f:
        for key in counter.keys():
            f.write(key + "\n")


#
# def get_syscalls():
#     counter = collections.Counter()
#     arr = []
#     with open("train/straceSamplesPos/output439.txt") as f:
#         lines = f.readlines()
#         for line in lines:
#             parts = line.split("(")
#             parts = parts[0].split(" ")
#             arr.append(parts[3])
#     counter.update(arr)
#     # print len(counter)
#     with open("syscalls.txt", "w") as f:
#         for key in counter.keys():
#             f.write(key + "\n")


def create_sysc2index():
    # get_syscalls()
    arr = []
    with open("syscalls.txt", "r") as f:
        lines = f.readlines()
    for line in lines:
        arr.append(line.strip("\n"))
    return {f: i for i, f in enumerate(arr)}  # syscall to indexes dictionary


def create_data_type(data_base, d_sysc2index, data_type):
    new_data = []
    for fname in os.listdir(data_base + '/straceSamples' + data_type):
        sysc = []
        with open(data_base + "straceSamples" + data_type + "/" + fname) as f:
            lines = f.readlines()
            arr = []
            for line in lines:
                parts = line.split("(")
                parts = parts[0].split(" ")
                # print parts
                arr.append(parts[3])
        for elem in arr:
            sysc.append(d_sysc2index.get(elem))
        # print cur
        new_data.append(sysc)
    return new_data


def read_data(database, d_sysc2index):
    data = []
    cur_sysc = ""
    for lab in ["Pos", "Neg"]:
        for fname in os.listdir(database + '/straceSamples' + lab):
            sysc = []
            with open(database + "/straceSamples" + lab + "/" + fname) as f:
                lines = f.readlines()
                for line in lines:
                    if line == "\n":
                        continue
                    parts = line.split("(")
                    parts = parts[0].split(" ")
                    # try:
                    if lab == "Pos":
                        cur_sysc = d_sysc2index.get(parts[2])
                        if cur_sysc == None:
                            try:
                                cur_sysc = d_sysc2index.get(parts[3])
                            except:
                                print parts
                            if cur_sysc == None:
                                print "pos", parts
                                print cur_sysc
                    else:
                        cur_sysc = d_sysc2index.get(parts[2])
                        if cur_sysc == None:
                            try:
                                cur_sysc = d_sysc2index.get(parts[3])
                            except:
                                print parts
                            if cur_sysc == None:
                                print "neg", parts
                                print cur_sysc  # print "neg", paneural-net-embedding.py:67rts[3]
                                # print cur_sysc
                    sysc.append(cur_sysc)
                    # except:
                    #     print lab, "here"
                    #     print parts
            data.append((sysc, lab))
    return data


def mlp(x):
    return layer2(layer1(x))


def layer1(x):
    W = parameter(pW1)
    b = parameter(pb1)
    return tanh(W * x + b)


def layer2(x):
    W = parameter(pW2)
    b = parameter(pb2)
    return W * x + b


def do_loss(probs, label):
    l = label
    return -log(pick(probs, l))


def classify(sen):
    # renew_cg()
    probs = mlp(rnn(sen))
    vals = probs.npvalue()
    return np.argmax(vals)


def rnn(seq):
    initial_s = builder.initial_state()
    first = E[V]
    prev_s = initial_s.add_input(first)
    # print seq
    for c in seq:
        try:
            cur_x = E[c]
            cur_s = prev_s.add_input(cur_x)
            prev_s = cur_s
        except:
            pass
    last = E[V + 1]
    final_s = prev_s.add_input(last)
    return final_s.output()


# def rnn(cur_samples):
#     initial_s = builder.initial_state()
#     first = E[0]
#     prev_s = initial_s.add_input(first)
#     for sample in cur_samples:
#         cur_x = vecInput(54)
#         cur_x.set(sample)
#         cur_s = prev_s.add_input(cur_x)
#         prev_s = cur_s
#     last = E[1]
#     final_s = prev_s.add_input(last)
#     return final_s.output()


def accuracy_on_dataset(dataset):
    good = bad = 0.0
    for sen, label in dataset:
        renew_cg()
        c = classify(sen)
        if c == l2i[label]:
            good += 1
        else:
            bad += 1
    return good / (good + bad)


if __name__ == "__main__":
    print "with all ftp also test no ftp"
    model = Model()
    NUM_LAYERS = 1
    INPUT_DIM = 7
    HIDDEN_DIM = 100
    HID = 50
    NOUT = 2
    l2i = {"Pos": 1, "Neg": 0}
    sysc2index = create_sysc2index()
    train = read_data("train", sysc2index)
    test = read_data("test", sysc2index)
    train_ftp = read_data("ftp", sysc2index)
    test_ftp = read_data("ftp-test", sysc2index)
    train_samba = read_data("samba", sysc2index)
    test_samba = read_data("samba-test", sysc2index)
    train.extend(train_ftp)
    train.extend(train_samba)
    # test.extend(test_ftp)
    # hard = read_data("hard", sysc2index)
    # cut = read_data("cut", sysc2index)
    # payload = read_data("new_payload", sysc2index)
    V = len(sysc2index)
    E = model.add_lookup_parameters((V + 2, INPUT_DIM))  # 5 number length vector for  each char (+ 2 padding).

    pW1 = model.add_parameters((HID, HIDDEN_DIM))
    pb1 = model.add_parameters(HID)
    pW2 = model.add_parameters((NOUT, HID))
    pb2 = model.add_parameters(NOUT)
    trainer = SimpleSGDTrainer(model)
    builder = LSTMBuilder(NUM_LAYERS, INPUT_DIM, HIDDEN_DIM, model)
    x = vecInput(INPUT_DIM)
    for i in range(100):
        total = 0
        random.shuffle(train)
        for samples, label in train:
            renew_cg()
            sen_vec = rnn(samples)
            probs = mlp(sen_vec)
            loss = pickneglogsoftmax(probs, l2i[label])
            total += loss.value()
            loss.backward()
            trainer.update()
        print "train done"
        train_acc = accuracy_on_dataset(train)
        print "test done"
        irc_acc = accuracy_on_dataset(test)
        ftp_acc = accuracy_on_dataset(test_ftp)
        print "ftp done"
        # hard_acc = accuracy_on_dataset(hard)
        # ftp_acc = accuracy_on_dataset(test_ftp)
        samba_acc = accuracy_on_dataset(test_samba)
        print "here"
        if irc_acc > 0.9:
            print "save"
            model.save("full-final")
        print "iteration: ", i + 1, ", loss: ", total / len(train), " accuracy on train: ", \
            train_acc, " accuracy on irc test: ", irc_acc, " accuracy on samba: ", samba_acc, " accuracy on ftp: ",\
            ftp_acc
