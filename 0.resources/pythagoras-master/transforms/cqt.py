# Author: Dan Valente

import numpy as np
from pythagoras.utils import utils
from pythagoras.filter_banks import constq
from pythagoras.transforms import stft


def cqt(x, frame_size=None, step_size=None, nfft=None, fs=44100, fmin=100,
        Q=34, n=12, kernel_taper='hamming'):
    """
        cqt(x, frame_size, step_size=None, nfft=None, fs=44100, fmin=100,
            Q=34, n=12, kernel_taper='hamming'):
            Constant-Q Transform
            Uses kernel algorithm specified in Brown & Puckette (1992)

        Input
        -----
            x:           input signal
            frame_size:  the size of an STFT frame in samples.  Default
                         is 1/10 of sample rate.
            step_size:   the 'hop' or step size in samples to move the
                         sliding window. Default is to half the frame
                         size.
            nfft:        number of points in the fft.  If none given, is
                         the next largest power of 2 larger than
                         frame_size.
            fs:          sample frequency
            fmin:        the base frequency (in Hz) upon which the
                         constant Q filter bank is based.
            Q:           the Q for each filter
            n:           number of Q bins (components) per octave

        Returns
        -------
            Constant-Q transform
        [REF]
        Brown JC and Puckette MS (1992). An efficient algorithm for the
        calculation of a constant Q transform. J. Acoust. Soc. Am.
        92(5):2698-2701
     """

    ## TODO: Test

    if frame_size is None:
        frame_size = fs/10

    if step_size is None:
        step_size = np.fix(frame_size/2)

    if step_size >= frame_size:
        raise

    if nfft is None:
        nfft = int(utils.nextpow2(len(x)))

    #Create the kernel (really, a filter bank that operates on STFT)
    qbank = constq(fmin, Q, n, fs, nfft, kernel_taper)

    # Take the STFT.  Honestly, you don't need to use a rectangular
    # taper, but if you choose another taper here, you'd essentially be
    # tapering twice. I don't think that would be much of a problem,
    # though, since it would effectively be a taper with sharper
    # transitions to zero.

    X = stft(x, frame_size, step_size=step_size, fs=44100, nfft=nfft,
             taper_name='rect')

    return (1./nfft) * np.dot(qbank, X)
