from math import factorial

import numpy as np
import pylab as pl
from obspy.signal import envelope
from scipy.signal import butter, filtfilt
from matplotlib.mlab import psd as psd_welch


def lowpass(signal, rate, cutoff):
    """Apply lowpass filter

    :param signal: numpy 1D array values of a signal
    :param rate: int sampling rate of the signal
    :param cutoff: int cutoff frequency 
    :return: numpy 1D array of filtered values
    """
    b, a = butter(2, cutoff/(rate/2.0), btype='low', analog=0, output='ba')
    return filtfilt(b, a, signal)


def normalize(signal):
    return (signal - np.mean(signal, axis=0))/np.std(signal, axis=0)


def autocorrelate(signal):
    """Perform autocorrelation on the signal using FFT

    :param signal: numpy 1D array values of the time varying signal
    :return: numpy 1D array autocorrelated signal
    """
    freqs = np.fft.rfft(signal)
    auto = freqs * np.conj(freqs)
    return np.fft.irfft(auto)


def psd(signal, rate):
    """Compute Power Spectral Density. Wrapper around matplotlib.mlab.psd which 
    computed PSD using Welch's average periodogram method with a block of 1024
    points for the FFT.
    More details - http://matplotlib.org/api/mlab_api.html#matplotlib.mlab.psd

    :param signal: numpy 1D array values of the time varying signal
    :param rate: sampling frequency of the signal
    :return: tuple (Pxx, freqs) meaning the magnitudes and the associated frequencies to them
    """
    return psd_welch(signal, NFFT=4096, Fs=rate, scale_by_freq=True)


def trim_psd(mags, freqs):
    """Clean up the Power Spectral Density by stripping low values from the back

    :param mags: numpy 1D array magnitudes
    :param freqs: numpy 1D array frequencies
    :return: tuple (mags, freqs) meaning the magnitudes and the associated frequencies to them
    """
    threshold = 0.1
    mags[mags < threshold] = 0
    new_mags = np.trim_zeros(mags, 'b')
    return new_mags, freqs[:new_mags.size]


def extract_local_maxima(mags, freqs):
    """Get the peak values from some specific bins in PSD

    :param mags: numpy 1D array magnitudes
    :param freqs: numpy 1D array frequencies
    :return: list of tuples (local_max_magniture, local_max_frequency)
    """
    freq_ranges = [(45, 55), (80, 90), (95, 105), (145, 155), (195, 205), (245, 255), (300, 310)]
    local_maximas = []
    for frange in freq_ranges:
        lower_limit = frange[0]
        upper_limit = frange[1]
        indices = np.where((freqs > lower_limit) & (freqs < upper_limit))[0]
        local_mags = []
        for i in indices:
            local_mags.extend([mags[i]])
        local_mags = np.array(local_mags)
        local_max_index = np.argmax(local_mags)
        if local_max_index == indices[0] or local_max_index == indices[-1]:
            local_maximas.extend([(0, 0)])
        else:
            local_max_mag = local_mags[local_max_index]
            index = indices[local_max_index]
            local_max_freq = freqs[index]
            local_maximas.extend([(local_max_mag, local_max_freq)])
    return local_maximas


def get_bin_areas(mags, freqs, window, limit=20):
    """Extract the area of integrating using composite trapezoidal rule

    :param mags: numpy 1D array magnitudes
    :param freqs: numpy 1D array frequencies
    :param window: int length of the bin window
    :return: list of area bins
    """
    bins = mags.size / window
    bin_areas = []
    bin_freqs = freqs[0:window]
    j = 0
    for i in xrange(bins):
        if i == limit:
            break
        try:
            bin_areas.extend([np.trapz(mags[j:j+window], x=bin_freqs)])
        except IndexError:
            pass
        j = i * window
    return bin_areas


def envelope(signal):
    """Extract the envelope of the signal

    :param signal: numpy 1D array values of the time varying signal
    :return: numpy 1D array envelope 
    """
    return envelope(signal)


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
