def autocorrelate(signal):
    """Perform autocorrelation on the signal using FFT

    :param signal: numpy 1D array values of the time varying signal
    :return: numpy 1D array autocorrelated signal
    """
    freqs = np.fft.rfft(signal)
    auto = freqs * np.conj(freqs)
    return np.fft.irfft(auto)