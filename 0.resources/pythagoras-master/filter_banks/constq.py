# Author: Dan Valente

import numpy as np
from pythagoras.utils import utils
from scipy import fft


def constq(fmin=100, Q=17, n=12, fs=44100, nfft=1024, taper_name='hamming'):
    """
        constq(fmin=100, Q=17, n=12, fs=44100, nfft=1024,
               taper_name='hamming')
            Calculates the filter bank (spectral kernel) for the
            Constant-Q Transform according to the method given in
            Brown & Puckette (1992).  Filter center frequencies range
            from fmin to fs/2 and are geometrically spaced according
            to n and Q.

            Input
            -----
                fmin:        the base frequency (in Hz) upon which the
                             filter bank is based.
                Q:           the Q for each filter
                n:           number of components per octave
                fs:          sample frequency (in Hz)
                nfft:        number of points in the fft of the
                             temporal kernels
                taper_name:  the name of the taper to use for the kernel

            Returns
            -------
                spectral kernel [2D np.array, size (Nq,nfft)]
                    where Nq is the number of frequency bins in the
                    Q transform

       [REF]
       Brown JC and Puckette MS (1992). An efficient algorithm for the
       calculation of a constant Q transform. J. Acoust. Soc. Am.
       92(5):2698-2701

    """
    #Number of components should only go up to the Nyquist frequency.
    #This is a function of fmin, as well as fs
    fk = []
    i = f = 0
    while (f <= fs/2):
        #Logarithmic spacing of frequencies.
        f = ((2 ** (1.0 / n)) ** i) * fmin
        fk.append(f)
        i += 1
        fk = np.array(fk)

    #Length of taper is frequency dependent
    N = (fs / fk) * Q

    kernel = np.zeros((len(fk), nfft), dtype='complex')
    for k in range(len(fk)):
        tap = utils.get_taper(taper_name, N[k])
        kstar = tap * np.exp(-1j * 2 * np.pi * Q * np.arange(N[k]) / N[k])
        kernel[k, :] = np.conj(fft(np.conj(kstar), nfft)) / N[k]

    return kernel
