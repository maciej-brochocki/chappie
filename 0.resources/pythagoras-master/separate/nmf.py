# Author: Dan Valente

import nimfa
from sklearn.decomposition import NMF


def nmf(X, method='sklearn', **nmfparams):
    """
    Calculates the non-negative matrix factorization of an input matrix
    """

    #TODO: Documentation

    if method == 'sklearn':
        model = NMF(**nmfparams)
        H = model.fit_transform(X)
        W = model.components_
    elif method == 'nimfa':
        model_tmp = nimfa.mf(X, **nmfparams)
        model = nimfa.mf_run(model_tmp)
        H = model.coef()
        W = model.basis()

    return (H, W, model)

if __name__ == "__main__":

    # Test NMF
    import scipy.io.wavfile as wv
    from pythagoras.transforms import stft
    import matplotlib.pyplot as plt
    import time
    import sys
    
    main_dir = sys.argv[1]
    data_dir = main_dir + "/data/"
    filename = "dylan_original.wav"

    (fs, dylan) = wv.read(data_dir + filename)
    dylan10 = dylan[:fs*10]
    (S, freq, t) = stft(dylan10, frame_size=2000, step_size=250, nfft=8192)

    sklearn_start = time.clock()
    #(sep_spect, sep_time, nmf_model) = nmf(abs(S), method='sklearn',
    #                                       n_components=2)
    (sep_spect, sep_time, nmf_model) = nmf(abs(S), method='nimfa',
                                           rank=2)
    sklearn_stop = time.clock()

    print sklearn_stop-sklearn_start
