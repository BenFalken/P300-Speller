try:
    print('trying to load workspace')
    kb_workspace_file  =  open('users/wspeier/p300 analyses/p300_kalman_bayes/kb_workspace_pos', 'rb')
    kb_workspace  =  pkl.load(kb_workspace_file)
    kb_workspace_file.close()
    print('workspace loaded')
except:
    print('workspace does not exist')
    folders = [
        'users/wspeier/Data/P300 data/p300_aniket/online/PF_2014_08_12001/',
        'users/wspeier/Data/P300 data/p300_aniket/online/PF_2014_08_08001/',
        'users/wspeier/Data/P300 data/p300_aniket/online/PF_2014_08_08b001/',
        'users/wspeier/Data/P300 data/p300_aniket/online/PF_2014_08_07001/',
        'users/wspeier/Data/P300 data/p300_aniket/online/PF_2014_04_19c001/',
        'users/wspeier/Data/P300 data/p300_aniket/online/PF_2014_04_19001/',
        'users/wspeier/Data/P300 data/p300_aniket/online/PF_2014_04_16001/',
        'users/wspeier/Data/P300 data/p300_aniket/online/PF_2014_04_19b001/',
        'users/wspeier/Data/P300 data/p300_pf/PF_2014_04_01001/',
        'users/wspeier/Data/P300 data/p300_pf/PF_2014_04_08001/',
        'users/wspeier/Data/P300 data/p300_pf/PF_2014_04_10001/',
        'users/wspeier/Data/P300 data/p300_pf/PF_2014_04_15001/',
        'users/wspeier/Data/P300 data/p300_pf/PF_2014_04_16001/',
        'users/wspeier/Data/P300 data/p300_pf/PF_2014_04_17001/',
        'users/wspeier/Data/P300 data/p300_pf/PF_2014_05_01b001/',
        'users/wspeier/Data/P300 data/p300_pf/PF_2014_05_01001/',
        'users/wspeier/Data/P300 data/p300_pf/PF_2014_05_06001/',
        'users/wspeier/Data/P300 data/p300_pf/PF_2014_05_15001/',
        'users/wspeier/Data/P300 data/p300_pf/PF_2014_05_30001/',
        'users/wspeier/Data/P300 data/p300_pf/PF_2014_06_11001/',
        ]
    signal_set = [[] for _ in range(len(folders))]
    states_set =  [[] for _ in range(len(folders))]
    parameters_set =  [[] for _ in range(len(folders))]

    for i in range(len(folders)):
        print('loading folder ' + folders[i])
        files = [file for file in os.listdir(directory + folders[i]) if file[-4:] == ".dat"]

        signal_set[i] = [[] for _ in range(len(files))]
        states_set[i] = [[] for _ in range(len(files))]
        parameters_set[i] =[[] for _ in range(len(files))]

        for j in range(len(files)):
            signal_set[i][j], states_set[i][j], parameters_set[i][j] = load_bcidat(folders[i] + files[j])
    
    file_info = {
        'signal_set': signal_set,
        'states_set': states_set,
        'parameters_set': parameters_set
    }

    kb_workspace_file = open('users/wspeier/p300 analyses/p300_kalman_bayes/kb_workspace_pos', 'ab')
    pkl.dump(kb_workspace_file, file_info)
    kb_workspace_file.close()

