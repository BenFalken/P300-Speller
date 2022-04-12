# returns answer,results,nStims,targets

def P300_kb_pos_classification(**kwargs): #filename, pmap, posmap, t_max, nPart):

    if 't_max' not in kwargs:
        t_max = 5*60
    if 'nPart' not in kwargs:
        nPart = 1000

    hp = 1
    thresh = 0.95
    p = 1/24

    [signal, states, parameters] = scipy.io.loadmat(filename)

    nr = parameters.NumMatrixColumns.NumericValue
    nc = parameters.NumMatrixRows.NumericValue
    rate = parameters.SamplingRate.NumericValue
    epochLength = parameters.EpochLength.NumericValue

    epochPoints = [[] for _ in range(int(epochLength * rate / 1000))]

    stimFlag1 = False
    stimFlag2 = False

    try:
        print(states.StimulusCode1)
        stimFlag1 = True
        try:
            print(states.StimulusCode3)
            stimFlag2 = True
        except Exception as e2:
            print('states does not contain StimulusCode3')
    except Exception as e:
        print('states does not contain StimulusCode1')

        # once you're bak online, find a solution
    [num, den] = butter(1,hp/(rate/2),'high')
    signal = filter(num,den,signal)

    t_start = rate*(parameters.PreRunDuration.NumericValue+parameters.PreSequenceDuration.NumericValue)+1
    t_end = np.min(t_start+t_max*rate, states.SelectedTarget.size)
    signal = signal[:t_end][:]

    stimulusType = states.StimulusType[:t_end]
    stimulusCode = double(states.StimulusCode[:t_end])

    if stimFlag1:
        stimulusCode1 = double(states.StimulusCode1[:t_end])
        stimulusCode2 = double(states.StimulusCode2[:t_end])
    else:
        stimulusCode1 = np.zeros(stimulusCode.size)
        stimulusCode2 = np.zeros(stimulusCode.size)

    if stimFlag2:
        stimulusCode3 = double(states.StimulusCode3[:t_end])
    else:
        stimulusCode3 = np.zeros(stimulusCode.size)

    rolled_stimulusCode = np.roll(stimulusCode)

    for i in range(stimulusCode.size):
        if stimulusCode[i] == rolled_stimulusCode[i]:
            stimulusCode = 0
            stimulusCode1 = 0
            stimulusCode2 = 0
            stimulusCode3 = 0

    onsetIndices = np.argwhere(stimulusCode > 0)

    allLabels = double(stimulusType[onsetIndices])
    allStim  = stimulusCode[onsetIndices]
    allStim1 = stimulusCode1[onsetIndices]
    allStim2 = stimulusCode2[onsetIndices]
    allStim3 = stimulusCode3[onsetIndices]

    transmitChList = parameters.TransmitChList.NumericValue
    classifier = parameters.Classifier.NumericValue
    aMean = parameters.AMean.NumericValue
    nMean = parameters.NMean.NumericValue
    asd = parameters.ASD.NumericValue
    nsd = parameters.NSD.NumericValue

    w = np.zeros((epochPoints, signal.shape[0]))

    for i in range(classifier.shape[0]):
        w[classifier[i][2], transmitChList[classifier[i][1]]] = classifier[i][4]

    allData = np.zeros((onsetIndices.size))
    for i in range(onsetIndices.size):
        insane_dot_product = signal[onsetIndices[i]+epochPoints-1][:].*w
        temp = np.sum(np.sum(onsetIndices[i]:insane_dot_product))
        allData[i] = temp

    a1 = states.SelectedTarget[t_start:t_end]
    rolled_a1 = np.roll(a1)

    for i in range(a1.size):
        if a1[i] == rolled_a1[i]:
            a1[i] = 0

    t_samples = np.max(np.argwhere(a1 > 0))

    cleaned_a1 = []

    for i in range(a1.size):
        if a1[i] != 0:
            cleaned_a1.append(a1[i])
    a1 = cleaned_a1

    chars = parameters.TargetDefinitions.Value[:][2]
    #a1 = chars(a1)

    letters = a1.size
    t = t_samples/parameters.SamplingRate.NumericValue

    rep = np.ceil(a1.size/target.size)
    t2 = ''
    for i in range(rep):
        t2 = t2 + target

    errors = letters - np.argwhere(a1 == t2[1:length[a1]]).size

    lambda_ = 0

    pos_map = {}
    pos_map['after'] = 'in'
    pos_map['block']= 'nn'
    pos_map['clear'] = 'jj'
    pos_map['daily'] = 'rb'
    pos_map['first'] = 'od'
    pos_map['giant'] = 'jj'
    pos_map['hours'] = 'nns'
    pos_map['minus'] = 'in'
    pos_map['noted'] = 'vbn'
    pos_map['panel'] = 'nns'
    pos_map['score'] = 'nn'
    pos_map['shown'] = 'vbn'
    pos_map['units'] = 'nns'

    allLabels = []
    allStim = []
    allStim1 = []
    allStim2 = []
    allStim3 = []
    allData = []
    allNStim = []
    allNLetters = []

    answer = [[] for _ in range(all_signals.size)] #cell(length(all_signals),1)
    results =  [[] for _ in range(all_signals.size*thresh.size)] #cell(length(all_signals),length(thresh))
    nStims = [[] for _ in range(all_signals.size*thresh.size)] #cell(length(all_signals),length(thresh))

    counter = 1
    index = 1

    for i in range(all_signals):
        print('Training file %d',i)

        fileLength = int(allData.shape[1]/all_signals.size)
        testIndices = (i-1)*fileLength+np.arange(fileLength)
        trainData = allData[:][setdiff[1:allData.shape[1][testIndices]]]
        trainLabels = allLabels[setdiff[1:allData.shape[1][testIndices]]]
        trainStim = allStim[setdiff[:allData.shape[1]][testIndices]]
        
        #[coeff1,feaSelector1] = BuildStepwiseLDA(trainData',trainLabels)

        if np.sum(coeff1) != 0:
            matmult_equal = np.matmult(trainData[feaSelector1][np.argwhere(trainLabels == 1)].T, coeff1)
             matmult_unequal = np.matmult(trainData[feaSelector1][np.argwhere(trainLabels != 1)].T, coeff1)
            attScore1 = np.min(1,np.max(-1,matmult_equal))
            nonScore1 = np.min(1,np.max(-1,matmult_unequal))
        else:
            attScore1 = normrnd(0,1,sum(trainLabels == 1),1)
            nonScore1 = normrnd(0,1,sum(trainLabels~= 1),1)

        attMean = np.mean(attScore1)
        nonMean = np.mean(nonScore1)
        attSD = np.std(attScore1)
        nonSD = np.std(nonScore1)
        
        TestSet = i

        print('Testing file %d',i)

        for j in range(TestSet):
            word = lower(parameters.TextToSpell.Value[0])
            wmap = pmap['t' + pos_map[str(word)]]
            answer[j] = np.zeros((1,allNLetters[j]))
            temp = parameters.TargetDefinitions.Value[:][1]

            for k in range(temp.size):
                if temp[k] == 'sp' :
                    temp[k] = '_'
                if temp[k].size > 0:
                    temp[k] = '0'
                try:
                    wmap['x' + temp[k]] = 0
                except:
                    temp[k] = '0'

            targets = lower(temp)
            
            pStrings = np.ones((nPart, thresh.size, allNLetters[j]))

            for k in range(thresh):
                nStims[j][k] = np.zeros((allNLetters[j]))

            for k in range(allNLetters[j]):
                print('Testing letter %d for file %d',k,i)
                answer[j][k] = targets[np.argwhere(targets == word(k))]
                
                nStim = np.ones((thresh.shape[0]*(-1)))
                priorProbs = np.zeros((nPart, thresh.size, targets.size))
                priorProbs2 = priorProbs

                for l in range(nPart):
                    for m = in range(thresh.size):
                        tstring = '_' + targets[pStrings[l][m][:(k-1)]].T
                        tstring = tstring[[np.argwhere(tstring == '_',1,'last')[0]+1]:]

                        for n in range(targets.size)
                            if not str('t' + tstring + targets[n]) in wmap:
                                wmap['t' + tstring + targets[n]] = 0

                            if not str('t' + tstring) in wmap:
                                wmap['t' + tstring] = 0

                            if wmap['t' + tstring] > -1*lambda_*targets.size:
                                priorProbs[l][m][n] = wmap['t' + tstring + targets[n]]
                            else:
                                priorProbs[l][m][n] = 0
                        priorProbs2[l][m][:] = 1/priorProbs2.shape[2[]]
                        priorProbs[l][m][:] = priorProbs[l][m][:]/np.sum(priorProbs[l][m][:])

                priorCDFs = np.zeros((nPart, thresh.size))
                priorRands = np.random.rand((nPart, thresh.size))
                priorProj = np.ones((nPart, thresh.size))*targets.size

                for l in range(targets.size):
                    priorCDFs = priorCDFs + priorProbs2[:][:][l]
                    criteria_fulfilled = np.zeros((priorProj.shape))

                    equality_indices = np.argwhere(priorProj == targets.size)
                    priorProj = np.zeros((nPart, thresh.size))
                    priorProj[equality_indices] = 1

                    equality_indices = np.argwhere(priorCDFs > priorRands)
                    priorCDFs[equality_indices] = 1

                    for i in range(criteria_fulfilled.shape[0]):
                        for j in range(criteria_fulfilled.shape[1]):
                            if priorProj[i][j] > 0 and priorCDFs > 0:
                                criteria_fulfilled[i][j] = l

                for l in range(nPart):
                    for m in np.argwhere(nStim<0).T:
                        pStrings[l][m][k] = priorProj[l][m]

                postProbs = -1*np.log(nPart)*np.ones((nPart, thresh.size))
                for l in np.argwhere(nStim<0).T:
                    for m in range(targets.size):
                        postProbs[np.argwhere(priorProj[:][l] == m)][l] += np.log(priorProbs[np.argwhere(priorProj[:][l] == m)][l][m]) - np.log(priorProbs2[np.argwhere(priorProj[:][l] == m)][l][m])

                postProbs -= np.log(np.ones((nPart))*np.sum(np.power(10, postProbs), 1))

                for l in np.argwhere(nStim<0).T:
                    for m in range(targets.size):
                        if np.sum(np.power(10, postProbs[np.argwhere(priorProj[:][l] == m)][l])) > thresh[l]:
                            nStim[l] = 0
                            nStims[j][l][k] = 0
                            postCDFs = 0
                            postRands = np.rand((nPart))
                            postProj = np.zeros((nPart))
                            for n in range(nPart):
                                postCDFs += np.power(10, postProbs[n][l])

                                equality_indices = np.argwhere(postProj == 0)
                                postProj[equality_indices] = 1

                                postRand_matrix = np.zeros((nPart))
                                equality_indices = np.argwhere(np.ones((nPart))*postCDFs > postRands)
                                postRand_matrix[equality_indices] = 1

                                for i in range(postProj.size):
                                    if postProj[i] > 0 and postRand_matrix[i] > 0:
                                        postProj[i] = n

                            pStrings[:][l][:] = pStrings[postProj][l][:]
                            break

                targetProbs = np.zeros((targets.size, 1))
                targetProbs2 = np.zeros((targets.size, allNStim[counter]))

                for l in range(allNStim[counter]):
                    score = np.min(1, np.max(-1, allData[feaSelector1][index].T*coeff1))
                    concatenated_array = np.concatenate(dec2bin(allStim3[index], 32), dec2bin(allStim1[index], 32), dec2bin(allStim1[index], 32))
                    temp = fliplr(concatenated_array)
                    for m in range(targets.size):
                        row = np.floor((m-1)/nc)+1
                        col = np.mod(m-1,nc)+1+nr

                        if or(and(or(allStim(index)  == row,allStim(index) == col),~stimFlag1),and(temp(m) == '1',stimFlag1))
                            targetProbs[m] + np.log(scipy.norm.pdf(score,attMean,attSD)) - np.log(scipy.norm.pdf(score,nonMean,nonSD))
            
                    targetProbs -= np.log(np.sum(np.power(10, targetProbs)))
                    targetProbs2[:][l] = targetProbs

                    for m in range(targets.size):
                        postProbs[np.argwhere(priorProj == m)] = targetProbs[m]

                    postProbs -= np.log(np.ones((nPart))*np.sum(np.power(10, postProbs),1))

                    for m in np.argwhere(nStim<0).T:
                        for n in range(targets.size):
                            if or(sum(power(10,postProbs(priorProj(:,m) =  = n,m)))>thresh(m),and(l =  = allNStim(counter),n =  = length(targets)))
                                nStim[m] = l
                                nStims[j][m][k] = l
                                postCDFs = 0
                                postRands = np.rand((nPart))
                                postProj = np.zeros((nPart))
                                for o in range(nPart):
                                    postCDFs = postCDFs + np.power(10, postProbs[o][m])

                                    equality_indices = np.argwhere(postProj == 0)
                                    postProj[equality_indices] = 1

                                    postCDF_matrix = np.zeros((nPart))
                                    equality_indices = np.argwhere(np.ones((nPart))*postCDFs > postRands)
                                    postCDF_matrix[equality_indices] = 1

                                    for i in range(nPart):
                                        if postProj[i] > 0 and postCDF_matrix[i] > 0:
                                            postProj[i] = o

                                pStrings[:][m][:] = pStrings[postProj][m][:]
                                break

                    index = index+1

                counter = counter+1

            for l in range(thresh.size):
                result = []
                for m in range(nPart):
                    try:
                        result['t' + targets[pStrings[m][l][:]].T] += 1/nPart
                    except:
                        result['t' + targets[pStrings[m][l][:]].T] = 1/nPart

                results[j][l] = result
    return answer, results, nStims, targets
