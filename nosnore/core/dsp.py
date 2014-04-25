import numpy as np 
import pylab as pl


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
