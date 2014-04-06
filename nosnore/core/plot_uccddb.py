import re
import numpy
import pylab as pl
import scipy.io as sio
from scipy import fft


def get_singal_info(name):
    """Extract signal information

    :param name: name of file that contains singal info
    :return: tuple of extracted data (signal interval, base, gain, units)
    """
    with open(name, "r") as f:
        info_lines = f.readlines()
    interval_regex = re.search(r"(\d+\.\d+)\Wsec", info_lines[3])
    interval = float(interval_regex.group(1))
    signal_data = re.split(r"\s", info_lines[5])
    gain = float(signal_data[2])
    base = int(signal_data[3])
    units = signal_data[4]
    return interval, gain, base, units


def get_mat_data(mat_name, base, gain):
    """Read and preprocess matlab data

    :param mat_name: the name of the file that holds mat data
    :param base: base of the signal
    :param gain: gain of the signal
    :return: preprocessed array of data
    """
    mat_data = sio.loadmat(mat_name)['val']
    mat_data = mat_data.astype(numpy.float)
    mat_data[mat_data==-32768] = numpy.nan
    for i, val in numpy.ndenumerate(mat_data):
        mat_data[i] = (mat_data[i] - base) / gain
    return mat_data


def get_timewave_data(name):
    """Compute and return timewave data - signal amplitude and time intervals

    :param name: filename of the signal to be processed
    """
    info_name = name + ".info"
    mat_name = name + ".mat"

    interval, gain, base, units = get_singal_info(info_name)
    mat_data = get_mat_data(mat_name, base, gain)
    x = numpy.arange(0, mat_data.shape[1]) * interval
    return mat_data, x


def plot_time_signal(name):
    """Plot a x,y graph of a sound time-expanded waveform

    :param name: filename of the signal to be ploted
    """
    mat_data, x = get_timewave_data(name)

    pl.plot(x, mat_data[0])
    pl.grid()
    pl.title("Recorded signal")
    pl.xlabel('Time (sec)')
    pl.ylabel('Sound signal (nd)')
    pl.show()


def get_autocorrelated_data(mat_data):
    """Compute and return autocorrelated signal

    :param mat_data: numpy array of signal data
    """
    n = mat_data.shape[0]
    R = numpy.zeros((n/2))
    for lag in xrange(0, n/2):
        x = mat_data[0:n-lag]
        y = mat_data[lag:]
        R[lag] = numpy.mean((x - numpy.mean(x)) * (y - numpy.mean(y)))/numpy.std(x)/numpy.std(y)
    return R


def plot_autocorrelated_signal(name):
    """Plot x,y graph of a sound signal that was autocorrelated

    :param name: filename of the signal to be processed
    """
    info_name = name + ".info"
    mat_name = name + ".mat"

    interval, gain, base, units = get_singal_info(info_name)
    mat_data = get_mat_data(mat_name, base, gain)
    x = numpy.arange(0, mat_data.shape[1]) * interval

    r = get_autocorrelated_data(mat_data[0][:2000])
    
    pl.plot(r)
    pl.grid()
    pl.title("Autocorrelation R(signal, signal_lag)")
    pl.show()

def get_psd_data(mat_data):
    """Compute and return power spectral density of the signal described by data

    :param mat_data: numpy array that describes the signal
    :return: power spectrum density data
    """
    return abs(fft(mat_data))


def plot_psd_signal(name):
    """Plot x,y graph of power spectral density of a sound signal

    :param name: filename of the signal to be processed
    """
    info_name = name + ".info"
    mat_name = name + ".mat"

    interval, gain, base, units = get_singal_info(info_name)
    mat_data = get_mat_data(mat_name, base, gain)
    psd = get_psd_data(mat_data[0])

    pl.plot(psd)
    pl.grid()
    pl.title("Power Spectral Density of the signal")
    pl.show()


def plot_all(name):
    info_name = name + ".info"
    mat_name = name + ".mat"

    interval, gain, base, units = get_singal_info(info_name)
    mat_data = get_mat_data(mat_name, base, gain)
    print "mat_data computed"
    time = numpy.arange(0, mat_data.shape[1]) * interval
    r = get_autocorrelated_data(mat_data[0][:40000])
    print "R computed"
    psd = get_psd_data(r)
    print "PSD computed"

    pl.figure(1)
    pl.subplot(311)
    pl.plot(time, mat_data[0])
    pl.grid()
    pl.title("Recorded signal")

    pl.subplot(312)
    pl.plot(r)
    pl.grid()
    pl.title("Autocorrelation of the signal")

    pl.subplot(313)
    pl.plot(psd)
    pl.grid()
    pl.title("Power Spectral Density of the signal")
    pl.show()


if __name__ == '__main__':
    # plot_time_signal('../samples/ucddb/short_sound_records/ucddb003_recm')
    # plot_autocorrelated_signal('../samples/ucddb/short_sound_records/ucddb003_recm')
    # plot_psd_signal('../samples/ucddb/short_sound_records/ucddb003_recm')
    plot_all('../samples/ucddb/short_sound_records/ucddb005_recm')
    # plot_all('../samples/ucddb/ucddb005_recm')
