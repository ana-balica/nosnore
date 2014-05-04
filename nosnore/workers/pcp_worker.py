# ---------------------------------------------------------------------------- #
# Test the functionality for PCP worker on 10 short signal chunks
# ---------------------------------------------------------------------------- #
import pprint

import numpy as np
import pylab as pl
from nosnore.core.dsp import autocorrelate, psd, smooth, detect_formants
from nosnore.core.signal import getwavdata, Signal
from nosnore.core.plot import subplot_start, subplot_continue, subplot_save, show_plot, save_plot_points
from nosnore.io.db import SqliteDatabase

from nosnore import log
logging = log.getLogger(__name__)

sqdb = SqliteDatabase("pcp_formants.db")
sqdb.execute("""CREATE TABLE formants (id integer primary key autoincrement, sid integer, 
                frequency real, power real)""", commit=True)

CHUNK_SIZE = 70000

pp = pprint.PrettyPrinter(indent=4)
files = ["nosnore/samples/cvut/01pcp_data.wav",
         "nosnore/samples/cvut/02pcp_data.wav",
         "nosnore/samples/cvut/03pcp_data.wav",
         "nosnore/samples/cvut/04pcp_data.wav",
         "nosnore/samples/cvut/05pcp_data.wav",
         "nosnore/samples/cvut/06pcp_data.wav"]

last = 0
for f in files:
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
        autocorr_sig = autocorrelate(signal.signal)
        psd_sig = psd(autocorr_sig, short_time)
        smoothed = smooth(psd_sig[1], window_size=81, order=4)
        for _ in xrange(20):
            smoothed = smooth(smoothed, window_size=81, order=4)
        maxtab, mintab = detect_formants(smoothed, psd_sig[0], delta=15)

        formants = []
        for peak in maxtab:
            formants.append((str(i+1), str(peak[0]), str(peak[1])))

        sqdb.executemany("INSERT INTO formants VALUES (NULL, ?, ?, ?)", formants)
        logging.info("Processed %02d" % (i+1))
    last = i+1

sqdb.close()
