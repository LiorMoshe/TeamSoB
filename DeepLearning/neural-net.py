from dynet import *
import numpy as np
import random
import os


def read_data(database):
    data = []
    for lab in ["Pos", "Neg"]:
        for dir_name in os.listdir(database + "/" + lab):
            for fname in os.listdir(database + "/" + lab + "/" + dir_name):
                new_samples = []
                new_samples.append(np.loadtxt(database + "/" + lab + "/" + dir_name + "/" + fname))
            data.append((lab, new_samples))
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


def rnn(cur_samples):
    initial_s = builder.initial_state()
    first = E[0]
    prev_s = initial_s.add_input(first)
    for sample in cur_samples:
        cur_x = vecInput(54)
        cur_x.set(sample)
        cur_s = prev_s.add_input(cur_x)
        prev_s = cur_s
    last = E[1]
    final_s = prev_s.add_input(last)
    return final_s.output()


def accuracy_on_dataset(dataset):
    good = bad = 0.0
    for label, sen in dataset:
        renew_cg()
        c = classify(sen)
        if c == l2i[label]:
            good += 1
        else:
            bad += 1
    return good / (good + bad)


if __name__ == "__main__":
    model = Model()
    data = read_data("train")
    NUM_LAYERS = 1
    INPUT_DIM = 54
    HIDDEN_DIM = 100
    HID = 5
    NOUT = 2
    l2i = {"Pos": 1, "Neg": 0}

    E = model.add_lookup_parameters((2, INPUT_DIM))  # 5 number length vector for  each char (+ 2 padding).

    pW1 = model.add_parameters((HID, HIDDEN_DIM))
    pb1 = model.add_parameters(HID)
    pW2 = model.add_parameters((NOUT, HID))
    pb2 = model.add_parameters(NOUT)
    trainer = SimpleSGDTrainer(model)
    builder = LSTMBuilder(NUM_LAYERS, INPUT_DIM, HIDDEN_DIM, model)
    x = vecInput(INPUT_DIM)
    for i in range(100):
        total = 0
        random.shuffle(data)
        for label, samples in data:
            renew_cg()
            sen_vec = rnn(samples)
            probs = mlp(sen_vec)
            loss = pickneglogsoftmax(probs, l2i[label])
            total += loss.value()
            loss.backward()
            trainer.update()
        print "iteration: ", i + 1, ", loss: ", total / len(data), " accuracy on train: ", accuracy_on_dataset(data)
