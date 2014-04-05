import re
import numpy
import pylab as pl
import scipy.io as sio


def plot_signal(name):
    """ Plot a x,y graph that shows a sound signal

    :param name: filename of the signal to be processed
    """
    info_name = name + ".info"
    mat_name = name + ".mat"

    with open(info_name, "r") as f:
        info_lines = f.readlines()
    interval, gain, base, units = parse_info(info_lines)
    mat_data = get_mat_data(mat_data, base, gain)
    x = numpy.arange(0, mat_data.shape[1]) * interval

    pl.plot(x, mat_data[0])
    pl.xlabel('Time (sec)')
    pl.ylabel('Sound signal ({0})'.format(units))
    pl.show()


def parse_info(info_lines):
    """ Extract signal information

    :param info_lines: array of strings representing lines of text from signal
                       info file
    :return: tuple of extracted data (signal interval, base, gain, units)
    """
    interval_regex = re.search(r"(\d+\.\d+)\Wsec", info_lines[3])
    interval = float(interval_regex.group(1))
    signal_data = re.split(r"\s", info_lines[5])
    gain = float(signal_data[2])
    base = int(signal_data[3])
    units = signal_data[4]
    return interval, gain, base, units


def get_mat_data(mat_name, base, gain):
    """ Read and preprocess matlab data

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


if __name__ == '__main__':
    plot_signal('../samples/ucddb/short_sound_records/ucddb002_recm')
