import numpy as np 
import pylab as pl
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


def get_envelope(signal):
    return envelope(signal)


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

