class PowerInitError(Exception):
    '''
    Exception rise if niether powers not power's range were given
    at initialization of Power object
    '''

    def __init__(self, pow_start, pow_stop, nop):
        message = str()
        if pow_start is None and pow_stop is None and nop is None:
            message = 'Neither power nor pow range ware given'
        elif pow_start is None and pow_stop is not None and nop is not None:
            message = 'Start power of the range wasn\'t given'
        elif pow_start is not None and pow_stop is None and nop is not None:
            message = 'Stop power of the range wasn\'t given'
        elif pow_start is not None and pow_stop is not None and nop is None:
            message = 'Number of points for range wasn\'t given'
        elif pow_start is None and pow_stop is None and nop is not None:
            message = 'Missing start and stop powers of the range'
        elif pow_start is not None and pow_stop is None and nop is None:
            message = 'Missing stop power and number of points for range'
        elif pow_start is None and pow_stop is not None and nop is None:
            message = 'Missing start power and number of points for range'
        else:
            message = 'Neither powers nor power\'s range ware given'

        super(PowerInitError, self).__init__(message)
