import scipy, os, re
import numpy as np
import pickle as pkl

directory = 'desktop/P300_data/'

try:
    print('trying to load workspace')
    kb_workspace_file = open(directory + 'kb_workspace')
    kb_workspace = pkl.load(kb_workspace_file)
    kb_workspace_file.close()
    print('workspace loaded')
except Exception as e:
    print('workspace does not exist')

    temp = os.listdir(directory)
    temp = temp[3:]
    folders = cell(temp.shape[0], 1)

    for i in range(temp.shape[0]):
        folders[i] = temp[i] + '/'

        # Come back to this later. Might be shitty syntax by setting everything empty

    bad_chans = [[] for _ in range(folders.size())] #cell(length(folders),1)
    signal_set = [[] for _ in range(folders.size())] #cell(length(folders),1)
    states_set = [[] for _ in range(folders.size())] #cell(length(folders),1)
    parameters_set = [[] for _ in range(folders.size())] #cell(length(folders),1)

    for i in range(folders.size):
        print('loading folder ' + folders[i])
        files = [file for file in os.listdir(directory + folders[i]) if file[-4:] == ".dat"]
        signal_set[i] = [[] for _ in range(files.shape[0])]
        states_set[i] = [[] for _ in range(files.shape[0])]
        parameters_set[i] = [[] for _ in range(files.shape[0])]

        for j in range(files.shape[0]):
            signal_set[i][j], states_set[i][j], parameters_set[i][j] = scipy.io.loadmat(directory + folders[i] + files[j][:])
    
        badChans[i] = []
    
    model_file = open('kb_workspace', 'ab')
    pkl.dump('kb_workspace', [signal_set, states_set, parameters_set, bad_chans])
    model_file.close()