from collections import namedtuple


import numpy as np 
import pylab as pl
from scipy.io import wavfile
from obspy.signal import envelope


def getwavdata(filename):
    return wavfile.read(filename)


FFT = namedtuple('FFT', 'freqs power')


class Signal(object):
    def __init__(self, signal, time):
        self.signal = signal
        self.size = signal.size
        self.time = time
        self.autocorr = None
        self.psd_ = None

        if self.size != self.time.size:
            raise Exception("X and Y axis should have same size")

    def split(self, window):
        start = 0
        end = window
        chunks = []
        while end < self.size:
            try:
                chunks.extend([self.signal[start:end]])
            except IndexError:
                chunks.extend([self.signal[start:]])
            start = end
            end += window
        return chunks

    def autocorrelate(self):
        freqs = np.fft.rfft(self.signal)
        auto = freqs * np.conj(freqs)
        self.autocorr = np.fft.irfft(auto)
        return self.autocorr

    def psd(self, autocorr=True):
        if autocorr:
            signal = self.autocorr
            if autocorr is None:
                raise ValueError("First perform autocorrelation")
        else:
            signal = self.signal
        datafft = np.fft.rfft(signal*np.hanning(self.size))
        datafft = abs(datafft)
        datafft = 10*np.log10(datafft)
        freqs = np.fft.fftfreq(self.size, self.time[1]-self.time[0])
        self.psd_ = FFT(freqs[:datafft.size-1], datafft[:-1])
        return self.psd_

    def envelope(self):
        return envelope(self.signal)
