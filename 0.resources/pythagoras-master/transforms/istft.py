#Author: Dan Valente

import numpy as np
from scipy.fftpack import ifft


def istft(X, fs, T, step_size=None):
    """
        istft

    """
    # TODO: Fix end-points and scaling
    # TODO: Check if same taper has to be applied after ifft as was applied in STFT
    # TODO: Error checks
    # TODO: Documentation

    y = np.zeros(T*fs)
    nfft = X.shape[0]

    for n, i in enumerate(range(0, len(y) - nfft, step_size)):
        y[i:i + nfft] += np.squeeze(np.real(ifft(X[:, n])))

    return y
