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

from nosnore import log
logging = log.getLogger(__name__)
pp = pprint.PrettyPrinter(indent=4)

db = SnoreDatabase("test_pcp_features.db")
db.create_features_table(7, 20)

filename_template = "nosnore/samples/cvut/short/%02d_pcp_snore.wav"

for i in xrange(20):
    logging.info("Signal chunk %02d" % (i+1))
    rate, data = getwavdata(filename_template % (i+1))
    n = data.size
    time = np.linspace(0, n/rate, num=n)
    signal = Signal(data, time)
    fsignal = lowpass(signal.signal, rate, 500)

    normalized = normalize(fsignal)
    auto_sig = autocorrelate(normalized)
    mags, freqs = psd(auto_sig, rate)
    peak_features = extract_local_maxima(mags, freqs)
    area_features = get_bin_areas(mags, freqs, 40)

    logging.info("Extracted {0} peak features".format(len(peak_features)))
    logging.info("Extracted {0} bin area features".format(len(area_features)))

    db.insert_signal_features(str(i+1), peak_features, area_features)

db.db.close()
