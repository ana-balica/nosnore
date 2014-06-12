def extract_local_maxima(mags, freqs, freq_ranges):
    """Get the peak values from some specific bins in PSD

    :param mags: numpy 1D array magnitudes
    :param freqs: numpy 1D array frequencies
    :param freq_ranges: list of tuples of format (lower_limit, upper_limit)
    :return: list of tuples (local_max_magniture, local_max_frequency)
    """
    local_maximas = []
    for frange in freq_ranges:
        lower_limit = frange[0]
        upper_limit = frange[1]
        indices = np.where((freqs > lower_limit) & (freqs < upper_limit))[0]
        local_mags = []
        for i in indices:
            local_mags.extend([mags[i]])
        local_mags = np.array(local_mags)
        local_max_index = np.argmax(local_mags)
        if local_max_index == indices[0] or local_max_index == indices[-1]:
            local_maximas.extend([(0, 0)])
        else:
            local_max_mag = local_mags[local_max_index]
            index = indices[local_max_index]
            local_max_freq = freqs[index]
            local_maximas.extend([(local_max_mag, local_max_freq)])
    return local_maximas