import numpy as np 
import pylab as pl
from scipy.io import wavfile
from nosnore.core.dsp import highpassfilter, autocorrelate, compute_psd, get_envelope


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


def plot_some_signals():
    f = "nosnore/samples/cvut/01pcp_data.wav"
    rate, data = getwavdata(f)
    n = data.size
    time = np.linspace(0, n/rate, num=n)
    chunks = make_chunks(data, 70000)
    for i, chunk in enumerate(chunks):
        # save the chunk in the time domain
        save_plot(chunk, str(i+1)+"snore.png", time[:chunk.size])
        autocorr = autocorrelate(chunk)
        x_vals, datafft = compute_psd(autocorr, time)
        # save the chunk after fft and autocorrelation
        save_plot(datafft, str(i+1)+"snore_fft.png", x_vals)
        # save the envelope of the signal
        env = get_envelope(chunk)
        save_plot(env, str(i+1)+"signal_envelope.png", time[:env.size])
        if i == 9:
            break

if __name__ == '__main__':
    files = ["nosnore/samples/cvut/01pcp_data.wav",
             "nosnore/samples/cvut/02pcp_data.wav",
             "nosnore/samples/cvut/03pcp_data.wav",
             "nosnore/samples/cvut/04pcp_data.wav",
             "nosnore/samples/cvut/05pcp_data.wav",
             "nosnore/samples/cvut/06pcp_data.wav"]

