import re
import numpy
import pylab as pl
import scipy.io as sio


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
    pl.xlabel('Time (sec)')
    pl.ylabel('Sound signal (nd)')
    pl.show()


def plot_frequency_signal(name):
    """Plot x,y graph of a sound signal in frequency domain

    :param name: filename of the signal to be processed
    """
    info_name = name + ".info"
    mat_name = name + ".mat"

    with open(info_name, "r") as f:
        info_lines = f.readlines()
    interval, gain, base, units = parse_info(info_lines)
    mat_data = get_mat_data(mat_name, base, gain)
    x = numpy.arange(0, mat_data.shape[1]) * interval

    print "starting autocorrelation"
    print mat_data[0][:3]
    cor_mat_data = numpy.correlate(mat_data[0][:100], mat_data[0][:100], "same")
    print len(cor_mat_data)
    print x.shape
    pl.plot(x[:100], cor_mat_data)
    pl.xlabel('Time (sec)')
    pl.ylabel('Sound signal ACF')
    # pl.show()


if __name__ == '__main__':
    plot_time_signal('../samples/ucddb/short_sound_records/ucddb003_recm')
    # plot_frequency_signal('../samples/ucddb/short_sound_records/ucddb003_recm')
