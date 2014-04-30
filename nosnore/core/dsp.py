import heapq
import numpy as np 
import pylab as pl
from operator import itemgetter
from obspy.signal import highpass, envelope


def autocorrelate(signal):
    freqs = np.fft.rfft(signal)
    auto = freqs * np.conj(freqs)
    return np.fft.irfft(auto)


def compute_psd(signal, time):
    datafft = np.fft.rfft(signal*np.hanning(len(signal)))
    datafft = abs(datafft)
    datafft = 10*np.log10(datafft)
    freqs = np.fft.fftfreq(signal.size, time[1]-time[0])
    return freqs[:datafft.size-1], datafft[:-1]


def smooth(signal, window_len=11, window='hanning'):
    if signal.ndim != 1:
            raise ValueError, "Smooth only accepts 1 dimension arrays."
    if signal.size < window_len:
            raise ValueError, "Input vector needs to be bigger than window size."
    if window_len < 3:
            return signal
    if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
            raise ValueError, "Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'"

    s = np.r_[2*signal[0]-signal[window_len-1::-1], signal, 2*signal[-1]-signal[-1:-window_len:-1]]
    if window == 'flat':
            w = np.ones(window_len,'d')
    else:  
            w = eval('np.'+window+'(window_len)')

    y = np.convolve(w/w.sum(), s, mode='same')
    return y[window_len:-window_len+1]


def get_envelope(signal):
    return envelope(signal)


def filter_features(features, n):
    features = [(power, freq) for power, freq in features if freq != 0]
    return heapq.nlargest(n, features, key=itemgetter(0))


def select_features(data, freqs):
    CHUNK_SIZE = 635
    start = 0
    end = CHUNK_SIZE
    chunks = []
    while end < data.size:
        try:
            chunks.extend([data[start:end]])
        except IndexError:
            chunks.extend([data[start:]])
        start = end
        end += CHUNK_SIZE
    features = []
    for i, chunk in enumerate(chunks):
        local_max = chunk.max()
        local_max_index = np.argmax(chunk)
        freq = freqs[local_max_index+(CHUNK_SIZE*i)]
        features.extend([(local_max, freq)])
    return features

