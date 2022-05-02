from load_kb_dataset import load_kb_dataset
from word_map2 import word_map2
from P300_kb_classification import P300_kb_classification
import numpy as np

wmap = word_map2()
thresh = [.98]

signal_set, states_set, parameters_set, bad_chans = load_kb_dataset()

accs = np.zeros((len(thresh), len(signal_set)))
trials = np.zeros((len(thresh), len(signal_set)))

answer = [[] for _ in signal_set]
results = [[] for _ in signal_set]
nStims = [[] for _ in signal_set]

for i in range(len(signal_set)):
    try:
        acc_sum = np.sum(accs[:][i])
    except:
        acc_sum = np.sum(accs[0][i])
    if acc_sum == 0:
        print('running subject %d' % i)
        print(accs)
        print(trials)
        channels = np.ones((32)) 
        for chan in bad_chans[i]:
            channels[chan] = 0

        answer[i], results[i], nStims[i], _ = P300_kb_classification(signal_set[i], states_set[i], parameters_set[i], channels, wmap, 1, 600, thresh, 50000)
                                          
        correct = np.zeros((results[i].shape[1]))
        total  = np.zeros((results[i].shape[1]))
        t  = np.zeros((results[i].shape[1]))
        for j in range(results[i].shape[0]):
            for k in range(results[i].shape[1]):
                keys = list(results[i][j][k].keys()) 
                maxV = 0
                maxI = 0
                for l in range(len(keys)):
                    if results[i][j][k][keys[l]] > maxV:
                        maxV = results[i][j][k][keys[l]]
                        maxI = l

                r = keys[maxI][:11]
                correct[k] += np.argwhere(r == '_' + answer[i][j][:10]).size
                total[k] += answer[i][j][:10].size
                t[k] += np.sum(nStims[i][j][k][:10])

        np.divide(correct, total, correct_divided_arr)
        accs[:][i] = correct_divided_arr

        np.divide(t, total, t_divided_arr)
        trials[:][i] = t_divided_arr
        print(accs)
        print(trials)
