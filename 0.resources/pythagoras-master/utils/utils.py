'''
Author: Dan Valente
Last modified: 2013-11-06

'''

import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as wv

def freq2mel(f):
    """
        freq2mel(f)
            Converts frequencies in Hz to the mel scale

        Input
        -----
            f:    frequency values in Hz

        Returns
        -------
            correpsonding mel values

    """

    return 2595 * np.log10(1 + f / 700.)


def mel2freq(m):
    """
        mel2freq(m)
            Converts mels back to frequencies in Hz

        Input
        -----
            m: mel values

        Returns
        -------
            corresponding frequency values

    """

    return 700 * (10 ** (m / 2595) - 1)


def nextpow2(x):
    """
        nextpow2(x)
            Calculates the next power of two greater than the number x

        Input
        -----
            x:    number you want get the next power of 2 of
                  should accept an array of numbers

        Returns
        -------
            The number which is the largest power of two greater than x
    """

    return 2 ** (np.ceil(np.log2(x)))


def get_taper(taper_name, N, param=1):
    """
        get_taper(taper_name,n,param=1)
            Calculates specified taper array
        Input
        -----
            taper_name:   name of the taper desired. Choices are:
                              rect
                              hamming
                              hanning
                              blackman
                              kaiser
                              gabor
            N:            length of the taper
            param:        if a taper requires parameters, they should
                          be input here.  Currently only supports the
                          alpha paramter of the Gabor taper
                          (as of 2013-11-07)

        Returns
        -------
            taper     [Length N np.array]

    """

    # TODO: Add in multitaper method
    # TODO: Should Gabor variance parameter be hard-coded?

    if taper_name == 'rect':
        return np.ones(N)
    elif taper_name == 'hamming':
        return np.hamming(N)
    elif taper_name == 'hanning':
        return np.hanning(N)
    elif taper_name == 'blackman':
        return np.blackman(N)
    elif taper_name == 'kaiser':
        return np.kaiser(N, param)
    elif taper_name == 'gabor':
        return np.exp(-np.pi
                      * ((np.linspace(0, N, N) - N/2) / param) ** 2)
    elif taper_name == 'mtm':
        return 'unfinished'


def plot_spectrogram(time, freq, X, fpass=None, tpass=None,
                     cmap_name='jet', log_plot=False):
    """
        plot_spectrogram(time,freq,X,fpass=None,tpass=None,
                  cmap_name='jet',log_plot = False)

            Plots the power spectrogram of the STFT.

            Input
            -----
                time:         time array
                freq:         frequency array
                X:            STFT
                fpass:        frequency limits to be shown, in form
                              [min max]
                tpass:        time limits to be shown, in form [min max]
                cmap_name:    name of the color map to use.  See
                              documentation from matplotlib color maps
                log_plot:     if True, then 10*log10(P) will be displayed
    """

    #plotting one-sided spectrogram, so multiply X by 2

    S = np.power(np.abs(2 * X), 2)

    if log_plot:
        S = 10 * np.log10(S)

    if fpass is None:
        fpass = [freq[0], freq[-1]/2]

    if tpass is None:
        tpass = [time[0], time[-1]]

    im = plt.imshow(S, aspect='auto',
                    extent=[time[0], time[-1], freq[0], freq[-1]],
                    origin='lower')
    im.set_cmap(cmap_name)
    ax = plt.gca()
    ax.set_xlim(tpass[0], tpass[1])
    ax.set_ylim(fpass[0], fpass[1])

    plt.xlabel("Time")
    plt.ylabel("Frequency")
    plt.show(block=False)

    return


def write_to_wav(x, fs=44100, filename='test'):
    # TODO: Documentation

    #Normalizes to max amplitude, ensures writable data type
    x = x/np.max(x)
    x = np.asarray(x, dtype=np.float32)
    wv.write(filename, fs, x)
