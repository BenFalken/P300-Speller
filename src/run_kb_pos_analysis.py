import pickle as pkl
import time

use_pos = False
map, pos_map = word_pos_map('data/brown/')
wmap = word_map2('data/brown/')

parameters_set[16][2].TextToSpell.Value[0] = ' THE LAZY '

thresh = [1,.99,.98,.97,.96,.95,.94,.93,.92,.91,.9]

if not (('accs' in globals() and 'var' in globals()) and ('accs' in locals() and 'var' in locals())):
    accs = np.zeros((thresh.size, signal_set.size))
    trials = np.zeros((thresh.size, signal_set.size))
    try:
        pos_file = open('p300 analyses/p300_kalman_bayes/kb_results_pos11')
        pos_11 = pkl.load(pos_file)
        pos_file.close()
    except:
        continue

if not use_pos:
    pos_map = {}
    pos_map['tstart'] = 1
    pos_map['tstart___start'] = 1
    pos_map['tstart___start___start'] = 1
    map = {}
    map['tstart'] = wmap

if not (('answer' in globals() and 'var' in globals()) and ('answer' in locals() and 'var' in locals())):
    answer = [[] for _ in range(signal_set.size)]
    results = [[] for _ in range(signal_set.size)]
    POSresults = [[] for _ in range(signal_set.size)]
    nStims = [[] for _ in range(signal_set.size)]

for i in range(signal_set.size):
    if np.sum(accs[:][i]) == 0:
        tic = time.time()
        print('running subject %d',i)
        print(accs)
        print(trials)
        channels = np.zeros((4))
        channels[:] = 1
        answer[i], results[i], POSresults[i], nStims[i], _ = P300_kb_pos_classification(signal_set[i], states_set[i], parameters_set[i], channels, map, pos_map, 1, 600,thresh,10000)
        
        correct = np.zeros((results[i].shape[1]))
        total  = np.zeros((results[i].shape[1]))
        t = np.zeros((results[i].shape[1]))
        a = ''

        for j in range(answer[i].shape[0]):
            a += answer[i][j]
        for k in range(results[i].shape[0]):
            keys = list(results[i][k].keys())
            maxV = 0
            maxI = 0
            for l in range(len(keys)):
                if results[i][k][keys[l]] > maxV:
                    maxV = results[i][k][keys[l]]
                    maxI = l

            r = keys[maxI]

            correct[k] += np.argwhere(r == '_' + a).size
            total[k] += len(a)
            for j in range(nStims[i].shape[0]):
                t[k] += np.sum(nStims[i][j][k])

        np.divide(correct, total, correct_divided_arr)
        accs[:][i] = correct_divided_arr

        np.divide(t, total, t_divided_arr)
        trials(:,i) = t_divided_arr

        print(accs)
        print(trials)

        file_info = {
            'accs': accs,
            'trials': trials,
            'answer': answer,
            'results': results,
            'POSresults': POSresults,
            'nStims': nStims,
            'use_pos': use_pos
        }

        save('p300 analyses/p300_kalman_bayes/kb_results_pos11', file_info)
        toc = time.time()
        print("Elapsed time: " + str(toc - tic) + " seconds")
