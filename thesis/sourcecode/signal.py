class Signal(object):
    """Encapsulates a signal wave
    """
    def __init__(self, signal, time):
        """Class initializer

        :param signal: 1D numpy array of signal data
        :param time: 1D numpy array of data representing the time
        """
        self._signal = signal
        self._size = signal.size
        self._time = time

        if self._size != self._time.size:
            raise ValueError("Signal dimensions should coincide")

    # setters and getters omitted from the example

    def split(self, window):
        """Split the signal into smaller chunks according to the window size

        :param window: int size of the chuck
        :return: list of chucks of signal data
        """
        start = 0
        end = window
        chunks = []
        while end < self.size:
            try:
                chunks.extend([self.signal[start:end]])
            except IndexError:
                chunks.extend([self.signal[start:]])
            start = end
            end += window
        return chunks
