# Author: Dan Valente

import numpy as np
from scipy.fftpack import ifft
from pythagoras.transforms import tfft
from pythagoras.utils import utils

def ceps(x, fs=44100, nfft=None, taper_name="rect", taper_param=1,
         which_type='power'):
    """
        ceps(x, fs=44100, nfft=None, taper_name="rect", taper_param=1,
             which_type='power'):
            Computes the cepstrum of the signal

        Input
        -----
            x:             real-valued signal
            fs:            sampling frequency of x
            nfft:          size of the fft
            taper_name:    the name of the taper to use.  Default is
                           rectangular ('rect'). See utils.get_taper for
                           options.
            taper_param:   parameter for taper. See utils.get_taper for
                           options
            which_type:    type of cepstrum, 'real' or 'power' ('complex'
                           not yet implemented')

        Returns
        -------
        (C,quef)
            C:     cepstrum
            quef:  quefrency vector
    """
    if nfft is None:
        nfft = int(utils.nextpow2(len(x)))

    X = tfft(x, nfft, taper_name, taper_param)

    if which_type == "real":
        logX = np.log(np.abs(X))
        C = np.real(ifft(logX))
    elif which_type == "power":
        logX = np.log(np.abs(X)**2)
        C = np.abs(ifft(logX))**2
    elif which_type == "complex":
        return "Complex cepstrum not yet implemented"

    quef = np.linspace(0, len(x)/fs, len(x))

    return C, quef
