# Author: Dan Valente

import numpy as np
from scipy.fftpack import fft
from pythagoras.utils import utils


def tfft(x, nfft=None, taper_name="rect", taper_param=None, one_sided=False):
    """
        tfft(x,nfft=None,taper_name="rect",taper_param=None,
             one_sided = False)
            Tapered FFT.
            This is basically a wrapper to scipy's fft, but allows
            user to choose a specific taper to be applied. Taper
            options can be found in utils.get_taper

        Input
        -----
            x:             the waveform to transform
            nfft:          number of points in the fft.  If none
                           given, the next largest power of 2 larger
                           than len(x) is used.
            taper_name:    the type of taper to use.  Default is
                           rectangular ('rect'). See utils.get_taper for
                           options.
            taper_param:   parameter for taper. See utils.get_taper for
                           options
            one_sided:     if True, yields the one-sided fourier transform

        Returns
        -------
            X:            one, or two sided tapered, fast Fourier transform
    """

    #TODO: Check magnitude on one-sided spectrum

    if nfft is None:
        nfft = int(utils.nextpow2(len(x)))

    taper = utils.get_taper(taper_name, len(x), taper_param)

    w = taper / sum(taper)

    X = fft(np.multiply(w, x), nfft)

    if one_sided:
        return 2*X[:nfft/2+1]
    else:
        return X
