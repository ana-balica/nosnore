# ---------------------------------------------------------------------------- #
# Test the functionality for PCP worker on 10 short signal chunks
# ---------------------------------------------------------------------------- #
import pprint

import numpy as np
import pylab as pl
from scipy.signal import find_peaks_cwt
from nosnore.core.dsp import autocorrelate, psd, smooth, detect_formants
from nosnore.core.signal import getwavdata, Signal
from nosnore.core.plot import subplot_start, subplot_continue, subplot_save, show_plot, save_plot_points

from nosnore import log
logging = log.getLogger(__name__)


CHUNK_SIZE = 70000


pp = pprint.PrettyPrinter(indent=4)
f = "nosnore/samples/cvut/01pcp_data.wav"

rate, data = getwavdata(f)
n = data.size
time = np.linspace(0, n/rate, num=n)
logging.info("Signal loaded with size {0}".format(n))

signal_main = Signal(data, time)
chunks = signal_main.split(CHUNK_SIZE)
logging.info("Signal split in {0} chunks".format(len(chunks)))
logging.info("Will process only 10 of them for testing purposes...")

chunks = chunks[:10]

for i, chunk in enumerate(chunks):
    short_time = time[:chunk.size]
    signal = Signal(chunk, short_time)
    autocorr_sig = autocorrelate(signal.signal)
    psd_sig = psd(autocorr_sig, short_time)
    smoothed = smooth(psd_sig[1], window_size=81, order=4)
    for _ in xrange(20):
        smoothed = smooth(smoothed, window_size=81, order=4)

    logging.info("Formants for signal %02d" % (i+1))
    maxtab, mintab = detect_formants(smoothed, psd_sig[0], delta=15)
    xm = [p[0] for p in maxtab]
    ym = [p[1] for p in maxtab]

    save_plot_points((psd_sig[0], smoothed), (xm, ym), 
                     "nosnore/images/pcp_results/%02d_pcp_snore_formants.png" % (i+1))

    subplot_start()
    subplot_continue(311, signal.signal, signal.time)
    subplot_continue(312, psd_sig[1], psd_sig[0])
    subplot_continue(313, smoothed, psd_sig[0])
    subplot_save("nosnore/images/pcp_results/%02d_pcp_snore.png" % (i+1))

    logging.info("Saved signal chunk %02d" % (i+1))
