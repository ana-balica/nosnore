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


if __name__ == '__main__':
    files = ["nosnore/samples/cvut/01pcp_data.wav",
             "nosnore/samples/cvut/02pcp_data.wav",
             "nosnore/samples/cvut/03pcp_data.wav",
             "nosnore/samples/cvut/04pcp_data.wav",
             "nosnore/samples/cvut/05pcp_data.wav",
             "nosnore/samples/cvut/06pcp_data.wav"]

    rate, data = getwavdata(files[0])
    n = data.size
    time = np.linspace(0, n/rate, num=n)
    chunks = make_chunks(data, 70000)
    for i, chunk in enumerate(chunks):
        autocorr = autocorrelate(chunk)
        x_vals, datafft = compute_psd(chunk, time[:chunk.size])
        # save_plot(datafft, str(i+1)+"snore.png")
        # if i == 10:
        #     break
