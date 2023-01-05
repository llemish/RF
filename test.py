import numpy as np
import pandas as pd
from matplotlib import pyplot
import seaborn as sns


class S2P:
    """
    class for handle standard S-matrix 2 x 2 for range of freqs

    Attributes:

        _matrix - matrix of S-params
            freqs - frequencies
            S11_Mag - S11 Magnitude (log?)
            S11_Phase - phase of S11
            S21_Mag
            S21_Phase
            S12_Mag
            S12_Phase
            S22_Mag
            S22_Phase

        _nop - nomber of points to measure
        _format - one of the DB, MA, RI
        _degree - True if angles in degrees, False - in radians
    """
    _NAMES_DB = ['freq', 'S11_Mag', 'S11_Phase', 'S12_Mag', 'S12_Phase',
                 'S21_Mag', 'S21_Phase', 'S22_Mag', 'S22_Phase']
    _NAMES_RI = ['freq', 'S11_Real', 'S11_Image', 'S12_Real', 'S12_Image',
                 'S21_Real', 'S21_Image', 'S22_Real', 'S22_Image']

    _NAMES = ['freq', 'S11', 'S12', 'S21', 'S22']

    def __init__(self, nop=None):

        self._matrix = None
        self._format = 'DB'
        self._degree = True

        if nop is not None:
            self._matrix = self._init_empty_matrix(nop)

    def _init_empty_matrix(self, nop):
        data_dict = {name: np.empty(nop, dtype=np.cfloat) for name in self._NAMES}
        matrix = pd.DataFrame.from_dict(data_dict)
        return matrix

    @property
    def format(self):
        return self._format

    @format.setter
    def format(self, value):
        if value in {'RI', 'MA', 'DB'}:
            self._format = value
        else:
            raise ValueError('Format must be one of RI, MA or DB')

    @property
    def degree(self):
        return self._degree

    @degree.setter
    def degree(self, value):
        if isinstance(value, bool):
            self._degree = value
        else:
            raise TypeError('Degree parameter must be bool')

    @property
    def S11(self):
        return self._return_Sparam(self._matrix['S11'].values)

    @property
    def S12(self):
        return self._return_Sparam(self._matrix['S12'].values)

    @property
    def S21(self):
        return self._return_Sparam(self._matrix['S21'].values)

    @property
    def S22(self):
        return self._return_Sparam(self._matrix['S22'].values)

    def from_list(self, data_list):
        if len(data_list) == 9 and self._len_check(data_list):
            data_dict = dict()
            if self._format in ['DB', 'MA']:
                names = self._NAMES_DB
            else:
                names = self._NAMES_RI
            for i in range(9):
                data_dict[names[i]] = np.asarray(data_list[i])
            self._from_dict(data_dict)
        else:
            raise ValueError('data_list must have 9 lists of the same length')

    def from_dict(self, data_dict):
        if self._format in ['DB', 'MA']:
            names = self._NAMES_DB
        else:
            names = self._NAMES_RI
        data_dict = {x: np.asarray(data_dict[x]) for x in data_dict}
        if all(x in names for x in data_dict.keys()):
            if self._len_check(data_dict):
                self._from_dict(data_dict)
            else:
                raise ValueError('All lists in dictionary must have the same length')
        else:
            raise ValueError('Incorrect keys in data dictionary')

    def _from_dict(self, data_dict):
        matrix_dict = dict()
        matrix_dict['freq'] = data_dict['freq']
        if self._format == 'DB':
            data_dict['S11_Mag'] = self.db2lin(data_dict['S11_Mag'])
            data_dict['S12_Mag'] = self.db2lin(data_dict['S12_Mag'])
            data_dict['S21_Mag'] = self.db2lin(data_dict['S21_Mag'])
            data_dict['S22_Mag'] = self.db2lin(data_dict['S22_Mag'])
        if self._format in {'DB', 'MA'}:
            if self._degree:
                data_dict['S11_Phase'] = self.degree2rad(data_dict['S11_Phase'])
                data_dict['S12_Phase'] = self.degree2rad(data_dict['S12_Phase'])
                data_dict['S21_Phase'] = self.degree2rad(data_dict['S21_Phase'])
                data_dict['S22_Phase'] = self.degree2rad(data_dict['S22_Phase'])
            matrix_dict['S11'] = data_dict['S11_Mag'] * np.exp(1j * data_dict['S11_Phase'])
            matrix_dict['S12'] = data_dict['S12_Mag'] * np.exp(1j * data_dict['S12_Phase'])
            matrix_dict['S21'] = data_dict['S21_Mag'] * np.exp(1j * data_dict['S21_Phase'])
            matrix_dict['S22'] = data_dict['S22_Mag'] * np.exp(1j * data_dict['S22_Phase'])
        elif self._format == 'RI':
            matrix_dict['S11'] = data_dict['S11_Real'] + 1j * data_dict['S11_Image']
            matrix_dict['S12'] = data_dict['S12_Real'] + 1j * data_dict['S12_Image']
            matrix_dict['S21'] = data_dict['S21_Real'] + 1j * data_dict['S21_Image']
            matrix_dict['S22'] = data_dict['S22_Real'] + 1j * data_dict['S22_Image']
        df = pd.DataFrame.from_dict(matrix_dict)
        self._matrix = df

    def lin2db(self, data):
        return 20 * np.log10(np.asarray(data))

    def db2lin(self, data):
        return 10 ** (data / 20)

    def degree2rad(self, angle):
        return (angle * np.pi) / 180

    def rad2degree(self, angle):
        return (angle * 180) / np.pi

    def from_dataframe(self, df):
        pass

    def from_s2p(self, path):
        pass

    def generate(self):
        pass

    def _len_check(self, data):
        ans = True
        if isinstance(data, dict):
            data_it = iter(data)
            the_len = len(data[next(data_it)])
            if not all(len(data[x]) == the_len for x in data_it):
                ans = False
        elif isinstance(data, (list, np.ndarray)):
            data_it = iter(data)
            the_len = len(next(data_it))
            if not all(len(x) == the_len for x in data_it):
                ans = False
        else:
            ans = False
        return ans

    def _return_Sparam(self, data):
        s_param = dict()
        data = np.asarray(data, dtype=np.cfloat)
        if self._format == 'RI':
            s_param['Real'] = np.real(data)
            s_param['Image'] = np.imag(data)
        elif self._format in {'DB', 'MA'}:
            s_param['Mag'] = np.abs(data)
            s_param['Phase'] = np.angle(data, deg=self._degree)
            if self._format == 'DB':
                s_param['Mag'] = self.lin2db(s_param['Mag'])
        return s_param



pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
a = S2P(nop=5)
print(a._matrix)
print('----------')
a.format = 'DB'
# a.from_dict({'freq': [1, 2, 3], 'S11_Mag': [1, 2, 3], 'S11_Phase': [1, 2, 3],
#              'S12_Mag': [12, 2, 3], 'S12_Phase': [1, 2, 3], 'S21_Mag': [1, 2, 3],
#              'S21_Phase': [1, 2, 3], 'S22_Mag': [1, 2, 3], 'S22_Phase': [1, 2, 3]})
a.from_list([[1, 2, 3], [1, 2, 3], [1, 2, 3],
             [30, 36, 42], [12, 87, -165], [1, 2, 3],
             [1, 2, 3], [1, 2, 3], [1, 2, 3]])
print(a._matrix)
a.format = 'DB'
# a.degree = False
print(a.S12)
