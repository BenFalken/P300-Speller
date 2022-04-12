wmap  =  word_map2('Data/brown/')
answer = [[] for _ in range(signal_set.size)]
results = [[] for _ in range(signal_set.size)]
nStims = [[] for _ in range(signal_set.size)]

thresh = np.arange(15)*12

accs = np.zeros((thresh.size, signal_set.size))
trials = np.zeros((thresh.size, signal_set.size))

for i in range(signal_set.size):
    print('running subject %d',i)
    channels = np.zeros((32))
    channels[:] = 1
    answer[i], results[i], nStims[i], _ =  P300_kb_static_classification(signal_set{i}, states_set{i}, parameters_set{i}, channels, wmap, 1, 600,thresh,1000)
    
    correct = np.zeros((results[i].shape[1]))
    total = np.zeros((results[i].shape[1]))
    t = np.zeros((results[i].shape[1]))

    for j in range(results[i].shape[0]):
        for k in range(results[i].shape[1]):
            keys = list(results[i][j][k].keys())
            maxV = 0
            maxI = 0
            for l in range(len(keys)):
                if results[i][j][k][keys[l]] >maxV:
                    maxV = results[i][j][k][keys[l]]
                    maxI = l

            r = keys[maxI]

            correct[k] += np.arghwhere(r == '_' + answer[i][j]).size
            total[k] += answer[i][j].size
            t[k] += np.sum(nStims[i][j][k])

    np.divide(correct, total, correct_divided_arr)
    accs[:][i] = correct_divided_arr

    np.divide(correct, total, t_divided_arr)
    trials[:][i] = t_divided_arr

