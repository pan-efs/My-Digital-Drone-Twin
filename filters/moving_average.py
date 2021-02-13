import numpy as np

class MovingAverage:
    
    def moving_average(self, coord, window):
        return np.convolve(coord, np.ones(window), 'valid') / window
