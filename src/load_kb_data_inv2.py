import os

print('workspace does not exist')

folders =  [
        'users/wspeier/Data/P300 data/p300_spanish/subject_3/PF32_2016_11_04_train32FF001/',
        'users/wspeier/Data/P300 data/p300_spanish/subject_4/PF32_2016_11_29_train32FF001/',
        'users/wspeier/Data/P300 data/p300_spanish/subject_5/PF32_2016_11_30_train32FF001/',
        'users/wspeier/Data/P300 data/p300_spanish/subject_6/PF32_2016_11_30b_train32FF001/',
        'users/wspeier/Data/P300 data/p300_spanish/subject_7/PF32_2016_12_01_train32FF001/',
        'users/wspeier/Data/P300 data/p300_spanish/subject_8/PF32_2016_12_05_train32FF001/',
        'users/wspeier/Data/P300 data/p300_spanish/subject_9/PF32_2016_12_07_train32FF001/',
        ]

signal_set = [[] for _ in range(len(folders))]
states_set =  [[] for _ in range(len(folders))]
parameters_set =  [[] for _ in range(len(folders))]
channels_set =  [[] for _ in range(len(folders))]

for i in range(len(folders)):
    print('loading folder ' + folders[i])
    files = [file for file in os.listdir(directory + folders[i]) if file[-4:] == ".dat"]
    
    signal_set[i] = [[] for _ in range(len(files))]
    states_set[i] = [[] for _ in range(len(files))]
    parameters_set[i] = [[] for _ in range(len(files))]
    for j in range(len(files)):
        signal_set[i][j], states_set[i][j], parameters_set[i][j] = load_bcidat(folders[i] + files[j])

    channels_set[i] = np.ones((32))

channels_set[3][16] = 0
channels_set[3][21] = 0
channels_set[3][25:29] = 0
channels_set[5][29] = 0
channels_set[7][22] = 0
channels_set[7][27] = 0
channels_set[7][28] = 0
