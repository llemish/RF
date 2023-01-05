import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import pyplot
import seaborn as sns

from frequency import Frequency


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
        _freq_suffix - one of the THz, GHz, MHz, kHz, Hz, mHz
    """
    _NAMES_DB = ['freq', 'S11_Mag', 'S11_Phase', 'S12_Mag', 'S12_Phase',
                 'S21_Mag', 'S21_Phase', 'S22_Mag', 'S22_Phase']
    _NAMES_RI = ['freq', 'S11_Real', 'S11_Image', 'S12_Real', 'S12_Image',
                 'S21_Real', 'S21_Image', 'S22_Real', 'S22_Image']

    _NAMES = ['freq', 'S11', 'S12', 'S21', 'S22']

    def __init__(self, nop=None):

        self._matrix = None
        self._fmatrix = None
        self._format = 'DB'
        self._degree = True
        self._suffix = 'Hz'

        if nop is not None:
            self._matrix = self._init_empty_matrix(nop)

    def __str__(self):
        text = 'S2P Object'
        return text

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
            self._init_fmatrix()
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
        return self._return_formatted_sparam('S11')

    @property
    def S11_(self):
        return self._matrix['S11'].values

    @property
    def S12(self):
        return self._return_formatted_sparam('S12')

    @property
    def S12_(self):
        return self._matrix['S12'].values

    @property
    def S21(self):
        return self._return_formatted_sparam('S21')

    @property
    def S21_(self):
        return self._matrix['S21'].values

    @property
    def S22(self):
        return self._return_formatted_sparam('S22')

    @property
    def S22_(self):
        return self._matrix['S22'].values

    @property
    def freq(self):
        freq = Frequency(freqs=self._matrix['freq'])
        freq.suffix = self._suffix
        return freq

    @property
    def matrix_(self):
        return self._matrix

    def _init_fmatrix(self):
        fmatrix = pd.DataFrame()
        fmatrix['freq'] = self._matrix['freq']
        if self._format == 'RI':
            for s_param in self._NAMES[1:]:
                fmatrix[s_param + '_Real'] = np.real(self._matrix[s_param])
                fmatrix[s_param + '_Image'] = np.imag(self._matrix[s_param])
        elif self._format in {'DB', 'MA'}:
            for s_param in self._NAMES[1:]:
                fmatrix[s_param + '_Mag'] = np.abs(self._matrix[s_param])
                fmatrix[s_param + '_Phase'] = np.angle(self._matrix[s_param], deg=self._degree)
                if self._format == 'DB':
                    fmatrix[s_param + '_Mag'] = self.lin2db(fmatrix[s_param + '_Mag'])
        self._fmatrix = fmatrix

    def from_list(self, data_list, freq_suffix='Hz', format='DB'):
        if len(data_list) == 9 and self._len_check(data_list):
            self._format = format
            data_dict = dict()
            if self._format in ['DB', 'MA']:
                names = self._NAMES_DB
            else:
                names = self._NAMES_RI
            for i in range(9):
                data_dict[names[i]] = np.asarray(data_list[i])
            self._from_dict(data_dict, freq_suffix)
            self._init_fmatrix()
        else:
            raise ValueError('data_list must have 9 lists of the same length')

    def from_dict(self, data_dict, freq_suffix='Hz', format='DB'):
        if format in ['DB', 'MA']:
            names = self._NAMES_DB
        else:
            names = self._NAMES_RI
        data_dict = {x: np.asarray(data_dict[x]) for x in data_dict}
        if all(x in names for x in data_dict.keys()):
            if self._len_check(data_dict):
                self._format = format
                self._from_dict(data_dict, freq_suffix)
                self._init_fmatrix()
            else:
                raise ValueError('All lists in dictionary must have the same length')
        else:
            raise ValueError('Incorrect keys in data dictionary')

    def _from_dict(self, data_dict, freq_suffix):
        self._suffix = freq_suffix
        matrix_dict = dict()
        freq = Frequency(freqs=data_dict['freq'], suffix=self._suffix)
        freq.suffix = 'Hz'
        matrix_dict['freq'] = freq.freqs
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

    def from_dataframe(self, df, freq_suffix='Hz', format='DB'):
        self.from_dict(df.to_dict(orient='list'), freq_suffix=freq_suffix, format=format)

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

    def _return_formatted_sparam(self, s_param_name):
        if self._format == 'RI':
            new_names = [s_param_name + '_Real', s_param_name + '_Image']
        else:
            new_names = [s_param_name + '_Mag', s_param_name + '_Phase']
        s_param = self._fmatrix[new_names]
        return s_param.to_dict(orient='list')

    def s2t(self):
        param = self._matrix
        param['det_s'] = param['S11'] * param['S22'] - param['S21'] * param['S12']
        param['T11'] = (-1 * param['det_s']) / param['S21']
        param['T12'] = param['S11'] / param['S21']
        param['T21'] = (-1 * param['S22']) / param['S21']
        param['T22'] = 1 / param['S21']
        param = param[['freq', 'T11', 'T12', 'T21', 'T22']]
        return param

    def plot(self, params, **kwargs):
        sns.set_theme()
        if isinstance(params, str):
            params = params.split(', ')
        plot_num = len(params)
        if plot_num > 1:
            nrow = (plot_num + 1) // 2
            ncol = 2 if plot_num > 1 else 1
            fig, axs = plt.subplots(nrow, ncol)
            for i in range(plot_num):
                cur_row = (i - 1) // 2
                cur_col = 1 if i > 1 else 0

                param = params[i]
                data = self._return_Sparam(self._matrix[param].values)
                freq = self.freq.freqs
                first = True
                for key in data:
                    if first:
                        axs[cur_row, cur_col].plot(freq, data[key])
                        axs[cur_row, cur_col].set_title(param)
                        first = False
                    else:
                        ax2 = axs[cur_row, cur_col].twinx()
                        ax2.plot(freq, data[key], color='orange')
        else:
            fig, ax = plt.subplots((plot_num + 1) // 2, 2 if plot_num > 1 else 1)
            data = self._return_Sparam(self._matrix[params[0]].values)
            freq = self.freq.freqs
            first = True
            for key in data:
                if first:
                    ax.plot(freq, data[key])
                    first = False
                else:
                    ax2 = ax.twinx()
                    ax2.plot(freq, data[key])
                ax.set_title(params[0])
        plt.show()




pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

x = pd.read_csv('s2p_example.csv')
# print(x.to_dict(orient='list'))
a = S2P()
a.from_dataframe(x, freq_suffix='GHz')
# a.format = 'RI'
a.plot(['S11', 'S12', 'S21', 'S22'])
print(a.S21)
