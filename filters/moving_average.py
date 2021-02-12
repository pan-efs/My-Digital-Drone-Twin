import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class MovingAverage:
    
    def moving_average(self, coord, window):
        return np.convolve(coord, np.ones(window), 'valid') / window


# Example
k = MovingAverage()
arr = [1,2,3]
ex = k.moving_average(arr,2)
print(ex)