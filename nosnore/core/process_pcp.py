import numpy as np 
import pylab as pl
from scipy.io import wavfile
from nosnore.core.dsp import autocorrelate, compute_psd


def getwavdata(filename):
    return wavfile.read(filename)


def make_chunks(data, window):
    start = 0
    end = window
    chunks = []
    while end < data.size:
        try:
            chunks.extend([data[start:end]])
        except IndexError:
            chunks.extend([data[start:]])
        start = end
        end += window
    return chunks


def save_plot(data, name, x_vals=None):
    pl.clf()
    if x_vals is not None:
        pl.plot(x_vals, data)
    else:
        pl.plot(data)
    pl.grid()
    pl.savefig(name)
