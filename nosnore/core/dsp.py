from collections import namedtuple
from math import factorial

import numpy as np
import pylab as pl
from obspy.signal import envelope


FFT = namedtuple('FFT', 'freqs power')


def autocorrelate(signal):
    """Perform autocorrelation on the signal using FFT

    :param signal: numpy 1D array values of the time varying signal
    :return: numpy 1D array autocorrelated signal
    """
    freqs = np.fft.rfft(signal)
    auto = freqs * np.conj(freqs)
    return np.fft.irfft(auto)
    

def psd(signal, time):
    """Compute Power Spectral Density

    :param signal: numpy 1D array values of the time varying signal
    :param time: numpy 1D array time
    :return: numpy 1D array power spectral density
    """
    size = signal.size
    datafft = np.fft.rfft(signal*np.hanning(size))
    datafft = abs(datafft)
    datafft = 10*np.log10(datafft)
    freqs = np.fft.fftfreq(size, time[1]-time[0])
    return FFT(freqs[:datafft.size-1], datafft[:-1])


def envelope(signal):
    """Extract the envelope of the signal

    :param signal: numpy 1D array values of the time varying signal
    :return: numpy 1D array envelope 
    """
    return envelope(signal)


def smooth(signal, window_size, order, deriv=0, rate=1):
    """Perform smoothing on the signal using Savitsky Golay Filtering
    Original source - http://wiki.scipy.org/Cookbook/SavitzkyGolay

    :param signal: numpy 1D array values of the time varying signal
    :param window_size: odd int length of the window
    :param order: int order of the polynomial used in the filtering 
    :param deriv: int order of the derivative to compute (default = 0 means only smoothing)
    :param rate: int rate
    :return: numpy 1D array smoothed signal varying in time
    """
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


def detect_formants(y_axis, x_axis=None, lookahead = 200, delta=0):
    """Detect formants (peaks) in a vector.
    A point will be considered a formant if it has the maximal or minimal value 
    and is preceded to the left by a value lower/larger than delta.
    Original source - https://gist.github.com/sixtenbe/1178136

    :param y_axis: numpy 1D array values of the time varying signal
    :param x_axis: numpy 1D array whose values correspond to the y_axis array and
                   is used in the return to specify the position of the formants.
    :param lookahead: int distance to look ahead from a formant candidate to
                      determine if it's an actual formants
    :param delta: int minimal difference between a formant and the following points
    :return: tuple of 2 lists containing the positive and the negative formants. 
             Each item of the list contains a tuple (position, formant_value)
    """
    max_peaks = []
    min_peaks = []
    dump = []

    length = len(y_axis)
    
    if lookahead < 1:
        raise ValueError, "Lookahead must be '1' or above in value"
    if not (np.isscalar(delta) and delta >= 0):
        raise ValueError, "delta must be a positive number"
    
    mn, mx = np.Inf, -np.Inf
    
    for index, (x, y) in enumerate(zip(x_axis[:-lookahead], y_axis[:-lookahead])):
        if y > mx:
            mx = y
            mxpos = x
        if y < mn:
            mn = y
            mnpos = x
        
        if y < mx-delta and mx != np.Inf:
            if y_axis[index:index+lookahead].max() < mx:
                max_peaks.append((mxpos, mx))
                dump.append(True)
                mx = np.Inf
                mn = np.Inf
                if index+lookahead >= length:
                    break
                continue
        
        if y > mn+delta and mn != -np.Inf:
            if y_axis[index:index+lookahead].min() > mn:
                min_peaks.append((mnpos, mn))
                dump.append(False)
                mn = -np.Inf
                mx = -np.Inf
                if index+lookahead >= length:
                    break
    
    try:
        if dump[0]:
            max_peaks.pop(0)
        else:
            min_peaks.pop(0)
        del dump
    except ValueError:
        pass
        
    return max_peaks, min_peaks
