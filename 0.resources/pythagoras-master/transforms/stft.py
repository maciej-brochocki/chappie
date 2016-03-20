# Author: Dan Valente

import numpy as np
from pythagoras.transforms import tfft
from pythagoras.utils import utils


def stft(x, frame_size=None, step_size=None, fs=44100, nfft=None,
         taper_name='rect', taper_param=None):
    """
         stft(x,frame_size=None,step_size=None,fs = 44100, nfft=None,
             taper_name='rect',taper_param=None)
            Calculates the Short-time Fourier Transform of the input
            signal x.

        Input
        -----
            x:             the waveform to transform
            frame_size:    the size of a frame in samples.  Defaults to
                           1/10 of sample rate.
            step_size:     the 'hop' or step size in samples to move the
                           sliding window. Default is to half the frame
                           size.
            fs:            sampling frequency of the signal.  Default is
                           44.1 kHz.
            nfft:          number of points in the fft.  If none given,
                           is the next largest power of 2 larger than
                           frame_size.
            taper_name:    the type of taper to use.  Default is
                           rectangular ('rect'). See utils.get_taper for
                           options.
            taper_param:   parameter for taper. See utils.get_taper for
                           options
        Returns
        -------
            (S,freq,time)
                S:         short-time Fourier transform
                freq:      frequency bins (in Hz)
                time:      time bins (in s)
    """

    if frame_size is None:
        frame_size = int(fs/10)

    frame_size = int(frame_size)

    if step_size is None:
        step_size = np.fix(frame_size/2)

    if step_size >= frame_size:
        raise

    if nfft is None:
        nfft = int(utils.nextpow2(frame_size))

    X = [tfft(x[i:i+frame_size], nfft, taper_name, taper_param)
         for i in range(0, len(x) - frame_size, step_size)]
    S = np.array(X)
    S = S.T

    freq = np.linspace(0, fs, nfft)
    time = np.linspace(0, len(x)/fs, len(x))

    return S, freq, time
