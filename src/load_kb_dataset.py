import os, re
import numpy as np
import pickle as pkl

from BCI2kReader import BCI2kReader as b2k
import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm 
from sklearn.preprocessing import scale
from sklearn.decomposition import PCA

def load_kb_dataset():
    directory = 'P300/'

    try:
        print('trying to load workspace')
        kb_workspace_file = open('kb_workspace')
        kb_workspace = pkl.load(kb_workspace_file)
        kb_workspace_file.close()

        signal_set = kb_workspace["signal_set"]
        states_set = kb_workspace["states_set"]
        parameters_set = kb_workspace["parameters_set"]
        bad_chans = kb_workspace["bad_chans"]

        print('workspace loaded')
    except Exception as e:
        print('workspace does not exist: ' + str(e))

        temp = os.listdir(directory)
        #temp = temp[3:]
        temp = temp[:10]
        folders = []

        for item in temp:
            folders.append(item + '/')

        bad_chans = []
        signal_set = []
        states_set = []
        parameters_set = []

        for i in range(len(folders)):
            print('loading folder ' + folders[i])

            files = []

            if folders[i] != '.DS_Store/' and folders[i] != 'kb_workspace':
                files = [file for file in os.listdir(directory + folders[i]) if file[-4:] == ".dat"]

            signal_set.append([[] for file in files])
            states_set.append([[] for file in files])
            parameters_set.append([[] for file in files])
            bad_chans.append([])
            
            for j in range(len(files)):
                data = directory + folders[i] + files[j]
                with b2k.BCI2kReader(data) as test: 
                    signal_set[i][j] = test.signals
                    states_set[i][j] = test.states
                    parameters_set[i][j] = test.parameters

        model_file = open('kb_workspace', 'ab')
        pkl.dump({"signal_set": signal_set, "states_set": states_set, "parameters_set": parameters_set, "bad_chans": bad_chans}, model_file)
        model_file.close()
        
    return signal_set, states_set, parameters_set, bad_chans



