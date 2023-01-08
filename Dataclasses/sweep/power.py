from dataclasses import dataclass

import numpy as np

from Exceptions.PowerInitException import PowerInitError


@dataclass(init=False)
class Power:
    """
    Dataclass for handling power sweep

    Attributes:
        _powers - array-like object that hold power's values
        _unit - one of {'dBm', 'W'}
        _nop - number of points
        _pow_start - the lowest power of range
        _pow_stop - the highest power of range
    """
    def __init__(self, powers=None, unit='dBm', nop=None, pow_start=None, pow_stop=None):
        self.unit = unit
        if powers is not None:
            self._powers = np.asarray(powers)
            self._nop = len(self._powers)
            self._pow_start = np.min(self._powers)
            self._pow_stop = np.max(self._powers)
        elif pow_start is not None and pow_stop is not None and nop is not None:
            self._nop = nop
            self._pow_start = pow_start
            self._pow_stop = pow_stop
            self._powers = np.linspace(self.pow_start, self.pow_stop, self.nop)
        else:
            raise PowerInitError(self.pow_start, self.pow_stop, self.nop)

    @property
    def unit(self):
        return self._unit

    @unit.setter
    def unit(self, value):
        if value in {'dBm', 'W'}:
            if value != self.unit:
                self._recalc_power(value)
            self._unit = value
        else:
            raise ValueError("Unit must be one of the {'dBm', 'W'}")

    @property
    def nop(self):
        return self._nop

    @property
    def pow_start(self):
        return self._pow_start

    @property
    def pow_stop(self):
        return self._pow_stop

    @property
    def powers(self):
        return self._powers

    def _recalc_power(self, value):
        pass
