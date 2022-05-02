import scipy
import numpy as np
from DownSampleMatByAvg import DownSampleMatByAvg

def DownSampleMatByPivot(sig, PivotPnts):
    segment = []
    numSegment = PivotPnts.size
    DSFactor = int(np.fix(sig.shape[0]/numSegment))

    l = PivotPnts.size
    asig = np.ones((l, sig.shape[1]))
    for k in range(sig.shape[1]):
        csig = scipy.signal.lfilter(np.ones((1,DSFactor))/DSFactor,1, sig[:][k])
        asig[:][k] = csig[PivotPnts]
    return [asig, t, segment]

def DownSample4Feature(sig, fnDownsample, DSFactor=0, nAvgTrial=1, Pivot=0):
    segment = []

    if sig is not None:     # dunno how else to test 'struct'ness rn
        numSegment = int(np.fix(sig.shape[0] / DSFactor))
        nTrials = sig.shape[1] 
        ix = np.arange(0, nTrials, nAvgTrial)
        if nTrials -  ix[-1] != nAvgTrial - 1:
            ix = ix[1:-2]
        nSmp = sig.shape[0]
        bsig = np.ones((nSmp, ix.size))

        for i in range(ix.size):
            if nAvgTrial <= 1:
                sig_mean = np.mean(sig[:, ix[i]:ix[i] + nAvgTrial - 1], axis=1)
            else:
                sig_mean = np.mean(sig[:, ix[i]:ix[i] + nAvgTrial - 1], axis=1)
            bsig[:, i] = sig_mean
        asig, t, segment= eval(fnDownsample)(bsig, numSegment)
    else:
        VarName = list(sig.keys(0))
        aCodeSig = sig[VarName[1]]
        ChanName =  list(aCodeSig.keys())
        ChanSig = aCodeSig[ChanName[1]]
        nRC = len(VarName)
        nChan = len(ChanName)
        nTrials = ChanSig.shape[1]

        downsamplematbypivot = 'DownSampleMatByPivot'

        if fnDownsample.lower() == downsamplematbypivot.lower():
            nSmp = len(Pivot[1])
        else:
            nSmp = int(np.fix(ChanSig.shape[0] / DSFactor))

        ix = np.arange(0, nTrials, nAvgTrial)

        if nTrials -  ix[-1] != nAvgTrial - 1:
            ix = ix[:-2]

        nOrigSmp = ChanSig.shape[0]

        bsig = np.ones((nOrigSmp, ix.size))
        nTrials = bsig.shape[1]

        for i in range(len(VarName)):
            aCodeSig = sig[VarName[i]]
            ChanName =  list(aCodeSig.keys())
            tsig = []
            for k in range(len(ChanName)):
                ChanSig = aCodeSig[ChanName[k]]
                afea = []
                numSegment = int(np.fix(ChanSig.shape[0] / DSFactor))

                for kk in range(ix.size):
                    bsig[:][kk] = np.mean(ChanSig[:][ix[kk]:ix[kk]+nAvgTrial-1], axis=1)

                if fnDownsample.lower() == downsamplematbypivot.lower():
                    afea = feval(fnDownsample, bsig, Pivot[k]) 
                else:
                    afea = feval(fnDownsample, bsig, numSegment) 

                tsig.extend(afea.T)

            rowIdx = np.arange((i-1)*nTrials+1, i*nTrials)
            asig[rowIdx][:] =  tsig

        t = np.arange(0, ChanSig.size, DSFactor)
        
    return asig, t, segment