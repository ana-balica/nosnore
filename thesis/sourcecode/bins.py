def get_bin_areas(mags, freqs, window, limit=20):
    """Extract the area of integrating using composite trapezoidal rule

    :param mags: numpy 1D array magnitudes
    :param freqs: numpy 1D array frequencies
    :param window: int length of the bin window
    :return: list of area bins
    """
    bins = mags.size / window
    bin_areas = []
    bin_freqs = freqs[0:window]
    j = 0
    for i in xrange(bins):
        if i == limit:
            break
        try:
            bin_areas.extend([np.trapz(mags[j:j+window], x=bin_freqs)])
        except IndexError:
            pass
        j = i * window
    return bin_areas