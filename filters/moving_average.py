import numpy as np

class MovingAverage:
    def __init__(self):
        pass
    
    def moving_average(self, coord, window):
        """
        Apply moving average filter to signal.
        
        :param coord: signal (desired coordinate, perhaps)
        :type coord: array
        :param window: size of filter window
        :type window: int
        :return: discrete, linear convolution of signal and window.
        :rtype: np.ndarray
        """
        return np.convolve(coord, np.ones(window), 'valid') / window