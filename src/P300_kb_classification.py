import scipy.signal
import numpy as np
from DownSample4Feature import DownSample4Feature

THRESH = [1, 0.999999999, 0.99999999, 0.9999999, 0.999999, 0.99999, 0.9999, 0.999, 0.998, 0.997, 0.995, 0.99, 0.98, 0.97, 0.96, 0.95, 0.94, 0.93, 0.92, 0.91, 0.9, 0.85, 0.8, 0.75, 0.7, 0.65, 0.6, 0.55, 0.5, 0.4, 0.3, 0.2, 0.1, 0]

def normpdf_python(x, mu, sigma):
   return 1/(sigma*np.sqrt(2*np.pi))*np.exp(-1*(x-mu)**2/ (2*sigma**2) )

def P300_kb_classification(all_signals, all_states, all_parameters, channels=None, wmap=0, hp=0, epochLength=None, thresh=THRESH, nPart=1000, nTrain=0, lambda_=0):
    all_signals = np.array(all_signals)
    try:
        signal = all_signals[0]
        parameters = all_parameters[0]
    except:
        return None, None, None, None

    if channels is None:
        channels = np.ones((signal.shape[1]))

    if hp == 0:
        hpflag = 0
    else:
        hpflag = 1

    if epochLength is None:
        epochLength = parameters['EpochLength']

    mapflag = 1

    nr = parameters['NumMatrixColumns'][0]
    nc = parameters['NumMatrixRows'][0]
    rate = parameters['SamplingRate']

    epochPoints = int(np.ceil(epochLength * rate / 1000))

    DSFactor = 12
    nAvgTrial = 1

    stimFlag1 = False
    stimFlag2 = False

    try:
        states = all_states[0]
        print(states['StimulusCode1'])
        stimFlag1 = True
        try:
            states['StimulusCode3']
            stimFlag2 = True
        except:
            print('states does not contain StimulusCode3')
    except:
        print('states does not contain StimulusCode1')

    allLabels = []
    allStim = []
    allStim1 = []
    allStim2 = []
    allStim3 = []
    allData = []
    allNStim = []
    allNLetters = []

    for i in range(all_signals.shape[0]):
        print('file number %d' % i)
        signal = np.array((all_signals[i][channels == 1][:]))
        if hpflag:
            b, a = scipy.signal.butter(1, 2*hp/rate, btype='highpass')
            signal = scipy.signal.lfilter(b, a, signal)
        
        states = all_states[i]
        parameters = all_parameters[i]
        
        stimulusType = states['StimulusType'][0]
        stimulusCode = states['StimulusCode'][0]
        
        if stimFlag1:
            stimulusCode1 = states['StimulusCode1'][0]
            stimulusCode2 = states['StimulusCode2'][0]
        else:
            stimulusCode1 = np.zeros((stimulusCode.size))
            stimulusCode2 = np.zeros((stimulusCode.size))
        
        if stimFlag2:
            stimulusCode3 = states['StimulusCode3'][0]
        else:
            stimulusCode3 = np.zeros((stimulusCode.size))
        
        circshift_equal_indices = np.argwhere(stimulusCode == np.roll(stimulusCode,1))[0]

        stimulusCode1[circshift_equal_indices] = 0
        stimulusCode2[circshift_equal_indices] = 0
        stimulusCode3[circshift_equal_indices] = 0
        stimulusCode[circshift_equal_indices] = 0
        
        onsetIndices = np.argwhere(stimulusCode > 0)

        word = parameters['TextToSpell'][1].lower()
        
        ends = [1]

        phaseInSeqArr = np.array(states['PhaseInSequence'])

        intersections = np.intersect1d(np.argwhere(phaseInSeqArr == 3), np.argwhere(np.roll(phaseInSeqArr, 1) != 3))

        for intersection in intersections:
            ends.append(intersection)

        onsetIndices = onsetIndices[onsetIndices < ends[-1]]

        tNStim = np.zeros((len(ends) - 1))

        for i in range(1, len(ends)):
            firstCondition = onsetIndices > ends[i - 1]
            secondCondition = onsetIndices < ends[i]
            intersectionOfConditions = firstCondition & secondCondition
            tNStim[i - 1] = np.sum(np.multiply(intersectionOfConditions, 1))
        
        onsetIndices = onsetIndices[:int(np.sum(tNStim))]
        
        allLabels.append(stimulusType[onsetIndices])
        allStim.append(stimulusCode[onsetIndices])
        allStim1.append(stimulusCode1[onsetIndices])
        allStim2.append(stimulusCode2[onsetIndices])
        allStim3.append(stimulusCode3[onsetIndices])
        allNStim.append(tNStim)
        allNLetters .append(len(word))
        
        for i in range(onsetIndices.size):
            temp = DownSample4Feature(signal[:, onsetIndices[i]:onsetIndices[i] + epochPoints - 1], 'DownSampleMatByAvg', DSFactor, nAvgTrial, [])
            allData.append(temp)

    allData = np.array(allData)
    allLabels = np.array(allLabels)

    answer = [[] for _ in all_signals]
    results =  [[[] for _ in thresh] for _ in all_signals]
    nStims = [[[] for _ in thresh] for _ in all_signals]

    counter = 1
    index = 1

    for i in range(len(all_signals)):
        print('Training file %d' % i)
        fileLength = allData.shape[1]/len(all_signals)
        testIndices = (i-1)*fileLength+np.arange(fileLength)
        trainData = allData[:][np.setdiff1d(np.arange(allData.shape[1]), testIndices)]
        trainLabels = allLabels[np.setdiff1d(np.arange(allData.shape[1]),testIndices)]
        trainStim = allStim[np.setdiff1d(np.arange(allData.shape[1]), testIndices)]
        
        ind_vals = [np.max(trainData[i]) for i in range(trainData.shape[0])]
        ind = np.array([1 if ind_vals[i] < 200 else 0 for i in range(len(ind_vals))])
        trainData = trainData[:][ind]
        trainLabels = trainLabels[ind]
        
        indices = np.random.permutation(trainLabels.size)
        if trainflag:
            indices = indices[:nTrain]
        
        
        trainData1 = trainData[:][indices]
        trainLabels1 = trainLabels[indices]
        coeff1, feaSelector1 = BuildStepwiseLDA(trainData1.T,trainLabels1)
        if coeff1 is not None:
            attScore1 = np.min(1, np.max(-1, trainData1(feaSelector1, np.argwhere(trainLabels1 == 1)).T*coeff1))
            nonScore1 = np.min(1, np.max(-1, trainData1(feaSelector1, np.argwhere(trainLabels1 != 1)).T*coeff1))
        else:
            attScore1 = normrnd(0, 1, np.argwhere(trainLabels1 == 1).shape[0], 1)
            nonScore1 = normrnd(0, 1, np.argwhere(trainLabels1 != 1).shape[0], 1)
        
        attMean = np.mean(attScore1)
        nonMean = np.mean(nonScore1)
        attSD = np.std(attScore1)
        nonSD = np.std(nonScore1)
        
        TestSet = i
        print('Testing file %d' % i)

        for j in range(TestSet, TestSet+1):
            parameters = all_parameters[j]
            word = parameters.TextToSpell.Value[0].replace(' ', '_')
            answer[j] = np.zeros((1, allNLetters[j]))
            temp = parameters.TargetDefinitions.Value[:][1]
            for k in range(len(temp)):
                if temp[k] == 'sp':
                    temp[k] = '_'
                
                if len(temp[k]) > 1:
                    temp[k] = '0'
                
                try:
                    wmap['x' + temp[k]] = 0
                except:
                    temp[k] = '0'
                
            
            targets = np.array([item.lower() for item in temp])
            
            pStrings = np.ones((nPart, thresh.size, allNLetters[j]))
            for k in range(thresh.size):
                nStims[j][k] = np.zeros((allNLetters[j]))
            
            for k in range(allNLetters[j]):
                print('Testing letter %d for file %d',k,i)
                answer[j][k] = targets[np.argwhere(targets == word[k])]
                print('Target character: ' + str(answer[j]))
                
                nStim = -1*np.ones((thresh.size))
                priorProbs = np.zeros(nPart, thresh.size,targets.size)
                for l in range(nPart):
                    for m in range(thresh.size):
                        tstring = '_' + targets[pStrings[l][m][1:k-1]].T
                        tstring = tstring[tstring.find('_')+1:]
                        for n in range(targets.size):
                            if str('t' + tstring + targets[n]) not in list(wmap.keys()):
                                wmap['t' + tstring + targets[n]] = 0
                            
                            if str('t' + tstring) not in list(wmap.keys()):
                                wmap['t' + tstring] = 0
                            
                            if wmap['t' + tstring] > -1*lambda_*targets.size:
                                priorProbs[l][m][n] += np.log10(wmap['t' + tstring + targets[n]] + lambda_) - np.log10(wmap['t' + tstring] + lambda_*targets.size)
                            else:
                                priorProbs[l][m][n] = np.log10(0)
                            
                        
                        priorProbs[l][m] -= np.log10(np.sum(np.power(10, priorProbs[l][m])))
                    
                priorCDFs = np.zeros(nPart, thresh.size)
                priorRands = np.random.rand(nPart, thresh.size)
                priorProj = np.ones(nPart, thresh.thresh)*targets.thresh

                for l in range(targets.size):
                    priorCDFs += np.power(10, np.priorProbs[:][:][l])
                    priorProj[np.intersect1d(np.argwhere(priorProj == targets.size), np.argwhere(priorCDFs > priorRands))] = l
                
                # Originally in the two loops, I moved it out
                nStimGreaterThanZero = [item for item in np.argwhere(nStim < 0)]

                for l in range(nPart):
                    for m in nStimGreaterThanZero:
                        pStrings[l][m][k] = priorProj[l][m]
                    
                
                postProbs = -1*np.log10((nPart))*np.ones((nPart, thresh.size))

                for l in nStimGreaterThanZero:
                    for m in range(targets.size):
                        if np.sum(np.power(10, postProbs[np.argwhere(priorProj[:][l] == m)][l])) > thresh[l]:
                            nStim[l] = 0
                            nStims[j][l][k] = 0
                            postCDFs = 0
                            postRands = np.random.rand(nPart,1)
                            postProj = np.zeros((nPart))
                            for n in range(nPart):
                                postCDFs += np.power(10, postProbs[n][l])
                                postProj[np.intersect1d(np.argwhere(postProj == 0), np.argwhere((np.ones((nPart))*postCDFs) > postRands))] = n
                            
                            pStrings[:][l][:] = pStrings[postProj][l][:]
                            break
                        
                targetProbs = np.zeros((targets.size))
                targetProbs2 = np.zeros((targets.size, allNStim[counter]))
                for l in range(allNStim[counter]):
                    score = np.min(1, np.max(-1, allData[feaSelector1][index].T*coeff1))
                    temp = np.fliplr([np.binary_repr(allStim3[index],32), np.binary_repr(allStim2[index],32), np.binary_repr(allStim1[index],32)])
                    for m in range(targets.size):
                        row = int(np.floor((m-1)/nc)+1)
                        col = int(np.mod(m-1,nc)+1+nr)
                        if ((allStim[index] == row or allStim[index] == col) and not stimFlag1) or (temp[m] == '1' and stimFlag1):
                            targetProbs[m] += np.log10(normpdf_python(score,attMean,attSD)) - np.log10(normpdf_python(score,nonMean,nonSD))
                        
                    
                    targetProbs = targetProbs - np.log10(np.sum(np.power(10,targetProbs)))
                    targetProbs2[:][l] = targetProbs
                    for m in range(targets.size):
                        postProbs[np.argwhere(priorProj == m)] = targetProbs[m]
                    
                    postProbs -= np.log10(np.ones(((nPart))*np.sum(np.power(10, postProbs))))

                    # le redeclaration
                    nStimGreaterThanZero = [item for item in np.argwhere(nStim < 0)]

                    for m in nStimGreaterThanZero:
                        for n in range(targets.size):
                            if np.sum(np.power(10,postProbs[np.argwhere(priorProj[:][m] == n)][m])) > thresh[m] or (l == allNStim[counter] and n == targets.size):
                                nStim[m] = l
                                nStims[j][m][k] = l
                                postCDFs = 0
                                postRands = np.random.rand((nPart))
                                postProj = np.zeros((nPart))
                                for o in range(nPart):
                                    postCDFs += np.power(10, postProbs[o][m])
                                    postProj[np.intersect1d(np.argwhere(postProj == 0),np.argwhere(np.ones((nPart))*postCDFs > postRands))] = o
                                
                                pStrings[:][m][:] = pStrings[postProj][m][:]
                                break
                            
                    index += 1
                counter += 1

                for l in range(1, 2):
                    result = []
                    for m in range(nPart):
                        try:
                            result['t' + targets[pStrings[m][l][:].T]] += 1/nPart
                        except:
                            result['t' + targets[pStrings[m][l][:].T]] = 1/nPart
                    print(result)
                
            
            for l in range(thresh.size):
                result = []
                for m in range(nPart):
                    try:
                        result['t' + targets[pStrings[m][l][:].T]] += 1/nPart
                    except:
                        result['t' + targets[pStrings[m][l][:].T]] = 1/nPart
                results[j][l] = result

    return answer,results,nStims,targets