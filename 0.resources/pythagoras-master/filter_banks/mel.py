# Author: Dan Valente

import numpy as np
from pythagoras.utils import utils
from scipy import fft


def mel(fstart=0, fs=44100, nfilt=40, nfft=8192):
    """
        mel(fstart=0,fs=44100,nfilt=40,nfft=8192)
            Creates the filter bank used for mapping frequency-domain
             energy in the STFT to the mel domain

        Input
        -----
            fstart:    the start frequency of the filter bank
            fs:        the sample rate
            nfilt:     the number of filters between fstart ans fs/2
            nfft:      the number of points used to calculate the STFT.
                        Make sure this matches with the number of points
                        in the STFT that you'll be filtering.

        Returns
        -------
            Filter bank [2D np.array, size (nfft/2+1,nfilt)]

        Note:
            There are numerous implementations of the mel-frequency
            filter bank. For a summary see [3]. In light of this, I have
            only implemented the simplest formulation, this is the one
            described in the European Telecommunications Standards
            Institute Technical Standard ES 201 108 v1.1.3 and in [3] as
            HTK MFCC FB-24

    REF
        [1] European Telecommunications Standards Institute Technical
            Standard ES 201 108 v1.1.3
        [2] http://www.practicalcryptography.com/miscellaneous/
            machine-learning/guide-mel-frequency-cepstral-coefficients
            -mfccs/
        [3] Ganchev T, Fakotakis N, and Kokkinakis G.  "Comparative
            evaluation of various MFCC implementations on the speaker
            verification task." In Proceedings of the SPECOM, vol. 1,
            pp. 191-194. 2005.
    """
    
    # Get vector of center frequencies
    m_start, m_end = utils.freq2mel(np.array([fstart, fs/2]))
    mc = np.linspace(m_start, m_end, nfilt + 2)  # +2 for the proper endpoints
    fc = utils.mel2freq(mc)

    # Convert center frequencies to bin numbers
    # The tutorial in [2] gives a formula for converting frequencies to
    # bin numbers that is slightly different than the ETSI ES 201-108
    # method.  I have chosen to use the method in the standard, as that
    # was the same one I derived, and don't quite see how the otherone
    # comes about. They don't give incredibly different center locations,
    # especially when nfft is large.  For small nfft, they are off by one
    # bin on many, but not all bins. Just FYI.

    # cbin = np.floor((nfft+1)*fc/fs))  [2] method.
    cbin = np.round(fc*nfft/fs)  # [1] method

    #Create filter bank matrix (carefully, since Python indexes from 0)
    #Size only goes up to Nyquist.
    fbank = np.zeros((nfft/2 + 1, nfilt))
    for k in range(1, nfilt + 1):
        for i in range(np.round(nfft/2 + 1) + 1):
            if (i >= cbin[k-1] and i <= cbin[k]):
                fbank[i, k-1] = (i - cbin[k-1]) / (cbin[k]-cbin[k-1])
            elif (i >= cbin[k] and i <= cbin[k+1]):
                fbank[i, k-1] = 1-(i-cbin[k])/(cbin[k+1]-cbin[k])

    return fbank
