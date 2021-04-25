import numpy as np

class MovingAverage:
    def __init__(self):
        pass
    
    def moving_average(self, coord, window):
        return np.convolve(coord, np.ones(window), 'valid') / window