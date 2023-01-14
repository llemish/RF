import numpy as np
import pandas as pd


class XNP:
    """
    _matrix - complex 2d-array
    _ports_number - int, number of ports
    _nop - number of points
    _z - float or list, impedance for ports
    _sweep_unit - frequency unit {THz, GHz, MHz, kHz, Hz}
                  time unit {s, ms, us, ns, ps}
                  date unit {date}
                  power unit {kW, W, mW, uW, dBm}
    _sweep_type - type of sweeping {freq, time, date, power}
    _sweep_ratio - ratio for recalculate sweep units to basic
    _parameter - kind of network data {S, Y, Z, H, G, T}
    _format - format of the data {DB, MA, RI}
    _use_fmatrix - boolean, show if use formatted matrix for speed up
    _fmatrix - formatted matrix
    """
    def __init__(self):
        self._matrix = np.empty(1, 1)
        self._port_number = 1
        self._nop = 0
        self.z = 50
        self._sweep_unit = 'HZ'
        self._sweep_type = 'freq'
        self._sweep_ratio = 1
        self._parameter = 'S'
        self._format = 'DB'
        self._use_fmatrix = False
        self._fmatrix = None

    @property
    def port_number(self):
        return self._port_number

    @port_number.setter
    def port_number(self, value):
        if isinstance(value, int):
            if value >= 1:
                self._port_number = value
            else:
                raise ValueError('Port Number must be one or greater')
        else:
            raise TypeError('Port number must be "int"')

    @property
    def nop(self):
        return self._nop

    @property
    def z(self):
        return self._z

    @z.setter
    def z(self, value):
        if isinstance(value, (list, tuple, np.ndarray, pd.Series)):
            self._init_z(value)
        elif isinstance(value, (int, float)):
            value = np.repeat(value, self._port_number)
            self._init_z(value)
        else:
            raise TypeError('Z0 must be numeric or list-like')

    def _init_z(self, value):
        if len(value) == self._port_number:
            self._z = value
        else:
            raise ValueError('Length Z must be equal to port number')

    @property
    def sweep_unit(self):
        return self._sweep_unit

    @sweep_unit.setter
    def sweep_unit(self, value):
        if isinstance(value, str):
            value = value.upper()
            if value in {'THZ', 'GHZ', 'MHZ', 'KHZ', 'HZ'}:
                self._sweep_type = 'freq'
                self._init_ratio()
            elif value in {'S', 'MS', 'US', 'NS', 'PS'}:
                self._sweep_type = 'time'
                self._init_ratio()
            elif value in {'DATE'}:
                self._sweep_type = 'date'
            elif value in {'KW', 'W', 'MW', 'UW', 'DBM'}:
                self._sweep_type = 'power'
                self._init_ratio()
            else:
                raise AttributeError('Unknown sweep unit')
            self._sweep_unit = value

    def _init_ratio(self):
        if self._sweep_unit in {'THZ'}:
            self._sweep_ratio = 10 ** 12
        elif self._sweep_unit in {'GHZ'}:
            self._sweep_ratio = 10 ** 9
        elif self._sweep_unit in {'MHZ'}:
            self._sweep_ratio = 10 ** 6
        elif self._sweep_unit in {'KHZ', 'KW'}:
            self._sweep_ratio = 10 ** 3
        elif self._sweep_unit in {'MW', 'MS'}:
            self._sweep_ratio = 10 ** -3
        elif self._sweep_unit in {'UW', 'US'}:
            self._sweep_ratio = 10 ** -6
        elif self._sweep_unit in {'NS'}:
            self._sweep_ratio = 10 ** -9
        elif self._sweep_unit in {'PS'}:
            self._sweep_ratio = 10 ** -12

    @property
    def sweep_type(self):
        return self._sweep_type

    @property
    def parameter(self):
        return self._parameter

    @parameter.setter
    def parameter(self, value):
        if value in {'S', 'Z', 'Y', 'H', 'G', 'T'}:
            self._parameter = value
        else:
            raise ValueError('Parameter must be one of {S, Y, Z, H, G, T}')

    @property
    def format(self):
        return self._format

    @format.setter
    def format(self, value):
        if value.upper() in {'DB', 'MA', 'RI'}:
            self._format = value.upper()
        else:
            raise ValueError('Format must be on of {DB, MA, RI}')

    @property
    def fmatrix(self):
        return self._use_fmatrix

    @fmatrix.setter
    def fmatrix(self, vlaue):
        if isinstance(vlaue, bool):
            self._use_fmatrix = vlaue
            if vlaue:
                self._create_fmatrix()
        else:
            raise TypeError('fmatrix must be boolean')

    def _create_fmatrix(self):
        pass


