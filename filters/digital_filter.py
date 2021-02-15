import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import *

class DigitalFilter:
    
    def digital_filter(self, xn: np.ndarray, n):
        b, a = butter(n, 0.05)
        zi = lfilter_zi(b, a)
        z, _ = lfilter(b, a, xn, zi = zi * xn[0])
        z2, _ = lfilter(b, a, z, zi = zi * z[0])
        y = filtfilt(b, a, xn)
        
        return z, z2, y
    
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
