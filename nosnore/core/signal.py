from collections import namedtuple


import numpy as np 
import pylab as pl
from scipy.io import wavfile
from obspy.signal import envelope


def getwavdata(filename):
    return wavfile.read(filename)


class Signal(object):
    def __init__(self, signal, time):
        self._signal = signal
        self._size = signal.size
        self._time = time

        if self._size != self._time.size:
            raise ValueError("Signal dimentions should coincide")

    @property
    def signal(self):
        return self._signal

    @signal.setter
    def signal(self, value):
        self._signal = value
    
    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        self._size = value
    
    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, value):
        self._time = value

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
