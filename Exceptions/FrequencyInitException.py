class FrequencyInitError(Exception):
    '''
    Exception rise if niether frequencies not frequancies range were given
    at initialization of Frequancy object
    '''

    def __init__(self, freq_start, freq_stop, nop):
        message = str()
        if freq_start is None and freq_stop is None and nop is None:
            message = 'Neither frequencies nor freq range ware given'
        elif freq_start is None and freq_stop is not None and nop is not None:
            message = 'Start frequency of the range wasn\'t given'
        elif freq_start is not None and freq_stop is None and nop is not None:
            message = 'Stop frequency of the range wasn\'t given'
        elif freq_start is not None and freq_stop is not None and nop is None:
            message = 'Number of points for range wasn\'t given'
        elif freq_start is None and freq_stop is None and nop is not None:
            message = 'Missing start and stop frequencies of the range'
        elif freq_start is not None and freq_stop is None and nop is None:
            message = 'Missing stop frequency and number of points for range'
        elif freq_start is None and freq_stop is not None and nop is None:
            message = 'Missing start frequency and number of points for range'
        else:
            message = 'Neither frequencies nor freq range ware given'

        super(FrequencyInitError, self).__init__(message)
