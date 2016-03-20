'''
Author: Dan Valente

'''

import numpy as np


def sine_wave(freq, phase=0, amplitude=1, length=1, fs=44100):
    """sine_wave(freq, phase=0,length=1,fs=44100)
    Creates a sine wave of specified frequency,sampling rate, phase,
    and length. Frequency is in Hz, Phase is in radians, length is in
    seconds, sampling rate is in Hz.

    Returns the waveform, time vector, and sampling rate as a tuple.
    """

    t = np.linspace(0, length, length*fs)
    x = amplitude * np.sin(2*np.pi*freq*t + phase)

    return x, t, fs


def linear_sweep(f_start, f_end, amplitude=1, length=1, fs=44100):
    """linear_sweep(f_start,f_end,length=1, fs=44100)
    Creates a unit amplitude linear sweep of length "length" seconds
    from f_start to f_end (frequencies in Hz).

    Returns the waveform, time vector, and sampling rate as a tuple.
    """
    t = np.linspace(0, length, length*fs)
    freq = 2*np.pi*((f_end - f_start)*t/length + f_start)
    x = amplitude * np.sin(np.multiply(freq, t))

    return x, t, fs


def rand_tones(f0=261.626, n_tones=12, max_tones_per_interval=None,
               interval_length=1, n_intervals=10, fs=44100):
    """
    Creates a song containing a superposition of randomly chosen tones in
    intervals of interval_length seconds. n_intervals is number of intervals
    """

    #TODO: Documentation

    if max_tones_per_interval is None:
        max_tones_per_interval = n_tones

    tone_bank = np.array([f0*2**(i/12.) for i in range(n_tones)])
    song = np.array([0])
    k = 1
    while (k <= n_intervals):
        #How many random tones in interval k?
        n_tones_in_interval = np.random.randint(1, max_tones_per_interval+1)
        #Sample tone bank without replacement
        np.random.shuffle(tone_bank)
        n = 1
        w = np.zeros(interval_length*fs)
        while (n <= n_tones_in_interval):
            #n random tones from set in this interval
            tmpw,time,sr = sine_wave(tone_bank[n],
                                     length=interval_length,
                                     fs=fs)
            w += tmpw
            n += 1
        song = np.concatenate([song, w])
        k += 1

    #return an amplitude normalized waveform
    return np.array(song)/np.max(song)
