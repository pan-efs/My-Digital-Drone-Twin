import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import *

class DigitalFilter:
    """
    Description: [text]:
    Filter data along one-dimension with an IIR or FIR filter.
    Filter a data sequence, xn, using a digital filter. 
    This works for many fundamental data types (including Object type). 
    The filter is a direct form II transposed implementation of the standard difference equation.
    
    Parameters: [array, int]: [signal, order]
    
    Returns: [z, z2, y]: [lfilter once, lfilter twice, filtfilt]
            *filtfilt = A forward-backward filter, to obtain a filter with linear phase.
    """
    def digital_filter(self, xn: np.ndarray, n):
        b, a = butter(n, 0.05)
        zi = lfilter_zi(b, a)
        z, _ = lfilter(b, a, xn, zi = zi * xn[0])
        z2, _ = lfilter(b, a, z, zi = zi * z[0])
        y = filtfilt(b, a, xn)
        
        return z, z2, y
    
    """
    Description: [text]:
    Visualize the returned parameters of digital_filter function.
    """
    def visualization(self, signal: np.ndarray, z, z2, y, title: str):
        plt.figure
        plt.plot(signal, 'b', alpha = 0.75)
        plt.plot(z, 'r--', z2, 'r', y, 'k')
        plt.legend(('noisy signal', 'lfilter, once', 'lfilter, twice',
            'filtfilt'), loc = 'best')
        plt.title(title)
        plt.xlabel('Frames')
        plt.ylabel('coords')
        plt.grid(True)
        plt.show()
