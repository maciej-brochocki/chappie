# Author: Dan Valente

import numpy as np
from scipy.fftpack import dct
from pythagoras.transforms import tfft
from pythagoras.filter_banks import mel


def mfcc(x, fs, fstart, nfft, nfilt):
    """
        mfcc
    """

    ## TODO: Test that mfcc gives proper coefficients
    ## TODO: Clean up / streamline input arguments
    ## TODO: Allow other FFT input arguments
    ## TODO: Documentation 

    #Take the FFT
    X = tfft(x, nfft)

    #Get one-sided spectrum
    S = np.abs(X[:nfft/2 + 1])
    #Generate filter bank
    mel_bank = mel(fstart, fs, nfilt, nfft)

    #Apply the filter bank
    S_filt = np.dot(mel_bank.T, S)

    #Log transform
    S_log = np.log(S_filt)

    #Discrete cosine transform to get the cepstral coefficients
    return dct(S_log)
