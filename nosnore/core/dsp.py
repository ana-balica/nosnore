from collections import namedtuple
from math import factorial

import numpy as np
import pylab as pl
from obspy.signal import envelope


FFT = namedtuple('FFT', 'freqs power')


def autocorrelate(signal):
    freqs = np.fft.rfft(signal)
    auto = freqs * np.conj(freqs)
    return np.fft.irfft(auto)
    

def psd(signal, time):
    size = signal.size
    datafft = np.fft.rfft(signal*np.hanning(size))
    datafft = abs(datafft)
    datafft = 10*np.log10(datafft)
    freqs = np.fft.fftfreq(size, time[1]-time[0])
    return FFT(freqs[:datafft.size-1], datafft[:-1])


def envelope(signal):
    return envelope(signal)


def smooth(signal, window_size, order, deriv=0, rate=1):
    try:
        window_size = np.abs(np.int(window_size))
        order = np.abs(np.int(order))
    except ValueError, msg:
        raise ValueError("Window_size and order have to be of type int")
    if window_size % 2 != 1 or window_size < 1:
        raise TypeError("Window_size size must be a positive odd number")
    if window_size < order + 2:
        raise TypeError("window_size is too small for the polynomials order")

    order_range = range(order+1)
    half_window = (window_size -1) // 2
    # precompute coefficients
    b = np.mat([[k**i for i in order_range] for k in range(-half_window, half_window+1)])
    m = np.linalg.pinv(b).A[deriv] * rate**deriv * factorial(deriv)
    # pad the signal at the extremes with
    # values taken from the signal itself
    firstvals = signal[0] - np.abs( signal[1:half_window+1][::-1] - signal[0] )
    lastvals = signal[-1] + np.abs(signal[-half_window-1:-1][::-1] - signal[-1])
    signal = np.concatenate((firstvals, signal, lastvals))
    return np.convolve( m[::-1], signal, mode='valid')


def detect_formants(signal, delta):
    maxtab = []
    mintab = []

    if delta <= 0:
        raise ValueError('Input argument delta must be a positive scalar')
    
    mn, mx = np.Inf, -np.Inf
    mnpos, mxpos = np.NaN, np.NaN
    
    lookformax = True
    x = np.arange(len(signal))
    for i in np.arange(len(signal)):
        this = signal[i]
        if this > mx:
            mx = this
            mxpos = x[i]
        if this < mn:
            mn = this
            mnpos = x[i]
        
        if lookformax:
            if this < mx-delta:
                maxtab.append((mxpos, mx))
                mn = this
                mnpos = x[i]
                lookformax = False
        else:
            if this > mn+delta:
                mintab.append((mnpos, mn))
                mx = this
                mxpos = x[i]
                lookformax = True

    return maxtab, mintab
