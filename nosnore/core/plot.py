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


def subplot_start():
    pl.clf()
    pl.figure(1)


def subplot_continue(count, y_vals, x_vals=None):
    pl.subplot(count)
    if x_vals is not None:
        pl.plot(x_vals, y_vals)
    else:
        pl.plot(y_vals)
    pl.grid()


def subplot_save(name):
    pl.savefig(name)
