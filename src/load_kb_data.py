import os
import pickle as pkl

try:
    print('trying to load workspace')
    kb_workspace_bs_file = open('/p300 analyses/p300_kalman_bayes/kb_workspace_bs', 'rb')
    kb_workspace_bs = pkl.load(kb_workspace_bs_file)
    kb_workspace_bs_file.close()
    print('workspace loaded')
except:
    print('workspace does not exist')

    folders =  [
        '/users/wspeier/Data/P300 data/p300_bs/subject_1/PF32_2016_11_04_train32FF001/', 
        '/users/wspeier/Data/P300 data/p300_bs/subject_2/PF32_2017_05_02_train32FF_125001/', 
        '/users/wspeier/Data/P300 data/p300_bs/subject_3/PF32_2017_05_09_train32FF_125001/', 
        '/users/wspeier/Data/P300 data/p300_bs/subject_4/PF32_2017_12_08_train32FF001/', 
        '/users/wspeier/Data/P300 data/p300_bs/subject_5/PF32_2018_01_19_train32FF001/', 
        '/users/wspeier/Data/P300 data/p300_bs/subject_6/PF32_2018_01_29_train32FF001/', 
        '/users/wspeier/Data/P300 data/p300_bs/subject_7/PF32_2018_04_19_train32FF001/', 
        '/users/wspeier/Data/P300 data/p300_bs/subject_8/PF32_2018_05_02_train32FF001/'
        ]

    signal_set = [[] for _ in range(len(folders))]
    states_set = [[] for _ in range(len(folders))]
    parameters_set = [[] for _ in range(len(folders))]

    for i in range(len(folders)):
        print('loading folder ' + folders[i])
        files = [file for file in os.listdir(directory + folders[i]) if file[-4:] == ".dat"]

        signal_set[i] = [[] for _ in range(len(files))]
        states_set[i] = [[] for _ in range(len(files))]
        parameters_set[i] = [[] for _ in range(len(files))]

        for j in range(len(files)):
            signal_set[i][j], states_set[i][j], parameters_set[i][j] = scipy.io.loadmat(folders[i] + files([j])

    badChans = [[], [], [7, 8, 18, 21, 23, 32], [31], [], [], [], [19, 29]]

    file_info = {
        'signal_set': signal_set,
        'states_set': states_set,
        'parameters_set': parameters_set
    }

    kb_workspace_bs_file = open('/users/Speier/Desktop/usb2/kb_workspace', 'ab')
    pkl.dump(kb_workspace_bs_file, file_info)
    kb_workspace_bs_file.close()