import pprint

import numpy as np 
import pylab as pl
from scipy.io import wavfile
from sklearn.decomposition import FastICA

from nosnore.core.dsp import autocorrelate, compute_psd, get_envelope, select_features, filter_features
from nosnore.io.csvdata import add_rows, read_feature_rows


def getwavdata(filename):
    return wavfile.read(filename)


def make_chunks(data, window):
    start = 0
    end = window
    chunks = []
    while end < data.size:
        try:
            chunks.extend([data[start:end]])
        except IndexError:
            chunks.extend([data[start:]])
        start = end
        end += window
    return chunks


def save_plot(data, name, x_vals=None):
    pl.clf()
    if x_vals is not None:
        pl.plot(x_vals, data)
    else:
        pl.plot(data)
    pl.grid()
    pl.savefig(name)


def show_plot(data, x_vals=None):
    pl.clf()
    if x_vals is not None:
        pl.plot(x_vals, data)
    else:
        pl.plot(data)
    pl.grid()
    pl.show()


def save_features(features, filename):
    with open(filename, "wb") as f:
        f.write("Power\t\t\t\t\tFrequency\n")
        for feature in features:
            f.write("{0}\t\t\t{1}\n".format(feature[0], feature[1]))


def plot_some_signals(data, time):
    chunks = make_chunks(data, 70000)
    for i, chunk in enumerate(chunks):
        # save the chunk in the time domain
        save_plot(chunk, str(i+1)+"snore.png", time[:chunk.size])
        autocorr = autocorrelate(chunk)
        x_vals, datafft = compute_psd(autocorr, time)
        # save the chunk after fft and autocorrelation
        save_plot(datafft, str(i+1)+"snore_fft.png", x_vals)
        # save the envelope of the signal
        env = get_envelope(chunk)
        save_plot(env, str(i+1)+"signal_envelope.png", time[:env.size])
        if i == 9:
            break


def add_noise(signal, time):
    other_signal = 5000 * np.sin(3*time)
    result = np.c_[signal, other_signal]
    result += 100 * np.random.normal(size=result.shape)
    mixing = np.array([[0, 1], [1, 1]])
    x_result = np.dot(result, mixing.T)

    pl.figure()
    pl.subplot(311)
    pl.plot(time, signal)
    pl.subplot(312)
    pl.plot(time, other_signal)
    pl.subplot(313)
    pl.plot(time, x_result)
    # pl.show()

    return x_result


def decompose(signal, components_count, time):
    estimator = FastICA(n_components=2)
    components = estimator.fit_transform(signal)
    
    pl.figure()
    pl.subplot(211)
    pl.plot(time, signal)
    pl.subplot(212)
    pl.plot(time, components)
    # pl.show()

    return components


def save_features(filename, sid, features, ica=False):
    rows = []
    for feature in features:
        rows.append([str(sid), feature[0], feature[1], ica])
    add_rows(filename, rows)


def get_features(signal, time):
    autocorr = autocorrelate(signal)
    freqs, datafft = compute_psd(autocorr, time)
    features = select_features(datafft, freqs)
    filtered_features = filter_features(features, 15)
    filtered_features.sort(key=lambda tup: tup[1])
    return filtered_features


def compare_features(filename, up, to):
    feature_frequency = dict()
    for i in xrange(up, to):
        print "Process chunk {0}".format(i)
        features = read_feature_rows(filename, i)
        features = [int(float(f)) for f in features]
        for f in features:
            if f in feature_frequency:
                feature_frequency[f] += 1
            else:
                feature_frequency[f] = 1
    return feature_frequency


def compare_features_after_ica(filename, up, to):
    results = dict()
    for i in xrange(up, to):
        features = read_feature_rows(filename, i)
        features = [int(float(f)) for f in features]
        features_ica = read_feature_rows(filename, i, True)
        features_ica = [int(float(f)) for f in features_ica]
        results[i] = len(set(features) & set(features_ica))
    return results


if __name__ == '__main__':
    pp = pprint.PrettyPrinter(indent=4)

    files = ["nosnore/samples/cvut/01pcp_data.wav",
             "nosnore/samples/cvut/02pcp_data.wav",
             "nosnore/samples/cvut/03pcp_data.wav",
             "nosnore/samples/cvut/04pcp_data.wav",
             "nosnore/samples/cvut/05pcp_data.wav",
             "nosnore/samples/cvut/06pcp_data.wav"]

    rate, data = getwavdata(files[0])
    n = data.size
    time = np.linspace(0, n/rate, num=n)

    sid = 100
    chunks = make_chunks(data, 70000)
    for i, chunk in enumerate(chunks):
        t = time[:chunk.size]
        features = get_features(chunk, t)
        save_features('nosnore/data/features_pcp.txt', sid+int(i), features)

        signal = add_noise(chunk, t)
        components = decompose(signal, 2, t)
        new_signal = components[:,1]
        features = get_features(new_signal, t)
        save_features('nosnore/data/features_pcp.py', sid+int(i), features, True)

        print "Chunk {0} features extracted and saved\n".format(sid+int(i))

    pp.pprint(compare_features('nosnore/data/features_pcp.txt', 100, 281))
    pp.pprint(compare_features_after_ica('nosnore/data/features_pcp.txt', 100, 281))