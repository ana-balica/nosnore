import pylab as pl


def show_plot(data, x_vals=None):
    pl.clf()
    if x_vals is not None:
        pl.plot(x_vals, data)
    else:
        pl.plot(data)
    pl.grid()
    pl.show()


def save_plot(data, name, x_vals=None):
    pl.clf()
    if x_vals is not None:
        pl.plot(x_vals, data)
    else:
        pl.plot(data)
    pl.grid()
    pl.savefig(name)


def save_signal_plots(signal, name):
    pl.clf()
    pl.figure(1)
    pl.subplot(311)
    pl.plot(signal.time, signal.signal)
    pl.grid()
    pl.subplot(312)
    pl.plot(signal.autocorr)
    pl.grid()
    pl.subplot(313)
    pl.plot(*signal.psd_)
    pl.grid()

    pl.savefig(name)
