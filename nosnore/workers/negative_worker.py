# ---------------------------------------------------------------------------- #
# Test the functionality for PCP worker on 10 short signal chunks
# ---------------------------------------------------------------------------- #
import pprint

import numpy as np
import pylab as pl
from nosnore.core.dsp import *
from nosnore.core.signal import getwavdata, savewavdata, Signal
from nosnore.core.plot import subplot_start, subplot_continue, subplot_save, show_plot, save_plot_points
from nosnore.io.db import SnoreDatabase

import logging
logging.basicConfig(filename='negative_worker.log',level=logging.DEBUG)


db = SnoreDatabase("negative_features.db")
db.create_features_table(7, 20)

CHUNK_SIZE = 70000

files = ["nosnore/samples/negative/01asleep.wav",
         "nosnore/samples/negative/02asleep.wav",
         "nosnore/samples/negative/03asleep.wav",
         "nosnore/samples/negative/04asleep.wav",
         "nosnore/samples/negative/05asleep.wav",
         "nosnore/samples/negative/06asleep.wav",
         "nosnore/samples/negative/07asleep.wav",
         "nosnore/samples/negative/08asleep.wav",
         "nosnore/samples/negative/09asleep.wav",
         ]

last = 0
for f in files:
    logging.info("Processing signal `{0}`".format(f))
    rate, data = getwavdata(f)
    n = data.size
    time = np.linspace(0, n/rate, num=n)
    logging.info("Signal loaded with size {0}".format(n))

    signal_main = Signal(data, time)
    chunks = signal_main.split(CHUNK_SIZE)
    logging.info("Signal split in {0} chunks".format(len(chunks)))


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

        logging.info("Extracted {0} peak features".format(len(peak_features)))
        logging.info("Extracted {0} bin area features".format(len(area_features)))

        db.insert_signal_features(str(i+1), peak_features, area_features)
    last = i+1

db.db.close()
