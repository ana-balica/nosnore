from scipy.io import wavfile
import numpy as np 
import pylab as pl
from scipy import fft


f = '../samples/snoring-3.wav'
rate, data = wavfile.read(f)


n = data.shape[0]
time = np.linspace(0, n/rate, num=n)

R = np.zeros((n/2))
for lag in xrange(0, n/2):
    x = data[0:n-lag]
    y = data[lag:]
    R[lag] = np.mean((x - np.mean(x)) * (y - np.mean(y)))/np.std(x)/np.std(y)

psd = abs(fft(R))

pl.figure(1)
pl.subplot(311)
pl.plot(time, data)
pl.grid()
pl.title("Snoring signal")

pl.subplot(312)
pl.plot(R)
pl.grid()
pl.title("Autocorrelation of the signal")

pl.subplot(313)
pl.plot(psd)
pl.grid()
pl.title("Power Spectral Density of the signal")
pl.show()