from dataclasses import dataclass

import numpy as np

from Exceptions.FrequencyInitException import FrequencyInitError


@dataclass(init=False)
class Frequency:
    """
    Dataclass for handling freqs

    Attributes:
        _freqs - array-like object that hold freq's values
        _suffix - One of [THz, GHz, MHz, kHz, Hz, mHz], default Hz
        _freq_start - the lowest freq of range
        _freq_stop - the highest freq of range
        _nop - number of points
        _w - boolean, True, if you use cyclic freq
        _log_freq - True if using logarithmic frequency, default False
        _ratio - numeric ration for calculating using suffix
    """

    def __init__(self, freqs=None, suffix='Hz', freq_start=None,
                 freq_stop=None, nop=None, w=False, log_freq=False):
        self.suffix = suffix
        self.w = w
        self.log_freq = log_freq

        if freqs is not None:
            freqs = np.asarray(freqs, dtype=float)
            if self._w:
                freqs = self.w2f(freqs)
            self._freqs = self._ratio * freqs
            self._nop = len(freqs)
            self._freq_start = np.min(self._freqs)
            self._freq_stop = np.max(self._freqs)
        elif freq_start is not None and freq_stop is not None and nop is not None:
            if w:
                freq_start = self.w2f(freq_start)
                freq_stop = self.w2f(freq_stop)
            self._nop = nop
            self._freq_start = freq_start * self._ratio
            self._freq_stop = freq_stop * self._ratio
            self._freqs = np.linspace(self._freq_start, self._freq_stop, num=self._nop)
        else:
            raise FrequencyInitError(freq_start, freq_stop, nop)

    def __str__(self):
        return str(self.freqs)

    def f2w(self, freq):
        return 2 * np.pi * freq

    def w2f(self, w):
        return w / (2 * np.pi)

    def _init_ratio(self):
        suffix = self.suffix
        if suffix == 'THz':
            ratio = 10 ** 12
        elif suffix == 'GHz':
            ratio = 10 ** 9
        elif suffix == 'MHz':
            ratio = 10 ** 6
        elif suffix == 'kHz':
            ratio = 10 ** 3
        elif suffix == 'mHz':
            ratio = 10 ** -3
        else:
            ratio = 1
        return ratio

    @property
    def suffix(self):
        return self._suffix

    @suffix.setter
    def suffix(self, value):
        if value in {'THz', 'GHz', 'MHz', 'kHz', 'Hz', 'mHz'}:
            self._suffix = value
            self._ratio = self._init_ratio()
        else:
            raise ValueError("suffix must be one of {THz, GHz, MHz, kHz, Hz, mHz}")

    @property
    def w(self):
        return self._w

    @w.setter
    def w(self, value):
        if type(value) == bool:
            self._w = value
        else:
            raise TypeError('w must be Boolean')

    @property
    def freqs(self):
        freqs = self._freqs
        if self._w:
            freqs = self.f2w(freqs)
        freqs = freqs / self._ratio
        return freqs

    def _return_freq(self, freq):
        if self._w:
            freq = self.f2w(freq)
        freq = freq / self._ratio
        return freq

    @property
    def freq_start(self):
        return self._return_freq(self._freq_start)

    @property
    def freq_stop(self):
        return self._return_freq(self._freq_stop)

    @property
    def nop(self):
        return self._nop

    @property
    def log_freq(self):
        return self._log_freq

    @log_freq.setter
    def log_freq(self, value):
        if isinstance(value, bool):
            self._log_freq=value
        else:
            raise TypeError('log_freq must be boolean')


# # fr = Frequency(freqs=[1, 2, 3, 4, 5], suffix='GHz')
# fr = Frequency(freq_start=2, freq_stop=4, nop=5, suffix='GHz')
# print(fr.suffix)
# fr.suffix = 'GHz'
# # fr.w = True
# print(fr.nop)
# print(fr.freq_start)
# print(fr.freq_stop)
# print(fr.freqs)
