CHUNK_SIZE = 70000

files = ["01pcp_data.wav",
         "02pcp_data.wav",
         # and other files listed here
         ]

last = 0
for f in files:
    rate, data = getwavdata(f)
    n = data.size
    time = np.linspace(0, n/rate, num=n)

    signal_main = Signal(data, time)
    chunks = signal_main.split(CHUNK_SIZE)

    for index, chunk in enumerate(chunks):
        i = last + index
        short_time = time[:chunk.size]

        signal = Signal(chunk, short_time)
        fsignal = lowpass(signal.signal, rate, 500)

        normalized = normalize(fsignal)
        auto_sig = autocorrelate(normalized)
        mags, freqs = psd(auto_sig, rate)
        peak_features = extract_local_maxima(mags, freqs)
        area_features = get_bin_areas(mags, freqs, 40)

    last = i+1