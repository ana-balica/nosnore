# ---------------------------------------------------------------------------- #
# Test the functionality for PCP worker on 10 short signal chunks
# ---------------------------------------------------------------------------- #
import pprint

import numpy as np
from nosnore.core.signal import getwavdata, Signal
from nosnore.core.plot import save_signal_plots
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
    signal.autocorrelate()
    signal.psd(autocorr=True)

    save_signal_plots(signal, "nosnore/images/pcp_results/%02d_pcp_snore.png" % (i+1))
    logging.info("Saved signal chunk %02d" % (i+1))
