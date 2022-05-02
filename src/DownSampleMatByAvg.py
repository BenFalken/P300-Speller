import scipy.signal
import numpy as np

def DownSampleMatByAvg(sig, numSegment):
    DSFactor = int(np.fix(sig.shape[0] / numSegment))
    afea = []
    segment = []
    for j in range(sig.shape[1]):
        csig = scipy.signal.lfilter(np.ones((DSFactor))/DSFactor, [1], sig[:, j])
        afea.extend(csig[np.arange(DSFactor, csig.size, DSFactor)])
    t = np.arange(sig.shape[0], DSFactor)
    return afea, t, segment