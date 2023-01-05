import numpy as np
import pandas as pd
from matplotlib import pyplot
import seaborn as sns

from frequency import Frequency
from s2p import S2P


class S2PComp(S2P):

    def __init__(self, s2p1, s2p2):
        if not isinstance(s2p1, S2P) or not isinstance(s2p2, S2P):
            raise TypeError('Both comparable objects must be S2P class')
        super(S2PComp, self).__init__()

        self._suffix = s2p1.freq.suffix
        self._format = s2p1.format
        self._degree = s2p1.degree

        m1 = s2p1.matrix_
        m2 = s2p2.matrix_
        self._matrix = pd.DataFrame()
        self._matrix['freq'] = m1['freq']
        self._matrix['S11_1'] = m1['S11']
        self._matrix['S11_2'] = m2['S11']
        self._matrix['S12_1'] = m1['S12']
        self._matrix['S12_2'] = m2['S12']
        self._matrix['S21_1'] = m1['S21']
        self._matrix['S21_2'] = m2['S21']
        self._matrix['S22_1'] = m1['S22']
        self._matrix['S22_2'] = m2['S22']
        self._matrix['S12_sum'] = self._matrix['S12_1'] + self._matrix['S12_2']
        self._matrix['S21_sum'] = self._matrix['S21_1'] + self._matrix['S21_2']
        self._matrix['S12_diff'] = self._matrix['S12_1'] - self._matrix['S12_2']
        self._matrix['S21_diff'] = self._matrix['S21_1'] - self._matrix['S21_2']

    @property
    def matrix_(self):
        return self._matrix

    @property
    def names(self):
        return self._matrix.columns.values

    def get(self, param):
        if param not in self.names:
            raise KeyError('Parameter must be in Object.names')
        param_value = self._get_param(param)
        return param_value

    def _get_param(self, param):
        ans = None
        if param == 'freq':
            ans = self.freq
        else:
            ans = self._return_Sparam(self._matrix[param].values)
        return ans


pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
a = S2P()
a.format = 'MA'
a.from_list([[1, 2, 3], [-22, -18, -15], [-45, 45, 135],
             [30, 36, 42], [12, 87, -165], [30, 36, 44],
             [12, 87, -167], [-23, -19, -16], [-45, 45, 135]], freq_suffix='GHz')
b = S2P()
b.format = 'MA'
b.from_list([[1, 2, 3], [-20, -16, -13], [-50, 40, 130],
             [28, 34, 40], [7, 80, -170], [28, 34, 42],
             [7, 80, -173], [-21, -17, -14], [-50, 40, 130]], freq_suffix='GHz')

c = S2PComp(a, b)
c.format = 'MA'
print(c.get('S21_diff'))
# print(c.matrix_)
