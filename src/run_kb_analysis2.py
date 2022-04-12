wmap = word_map2('desktop/brown/')
thresh = [.98]

accs = zeros(length(thresh),length(signal_set))
trials = zeros(length(thresh),length(signal_set))

answer = [[] for _ in range(signal_set.size)]
results = [[] for _ in range(signal_set.size)]
nStims = [[] for _ in range(signal_set.size)]

for i in range(signal_set.size):
    if np.sum(accs[:][i]) == 0:
        print('running subject %d',i)
        print(accs)
        print(trials)
        channels = zeros((32)) 
        channels[:] = 1
        channels[badChans[i]] = 0

        answer[i], results[i], nStims[i], _ = P300_kb_classification_temp(signal_set[i], states_set[i], parameters_set[i], channels, wmap, 1, 600, thresh, 50000)
                                                                                
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