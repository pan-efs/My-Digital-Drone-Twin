import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.signal import *

class DigitalFilter:
    def __init__(self):
        pass
    
    def digital_filter(self, xn: np.ndarray, n):
        """
        Design a digital filter.
        Find the coefficients of initial states.
        Filter data along one-dimension with an IIR. Filter a data sequence, xn, using a digital filter.
        Apply a forward-backward filter, to obtain a filter with linear phase.
        
        :param xn: signal
        :type xn: np.ndarray
        :param n: order of filter
        :type n: int
        
        :return: z: output of digital filter, z2: output of digital filter based on z's output, 
                y: the filtered output with the same shape as signal.
        :rtype: z: array, z2: array, y: np.ndarray
        """
        
        b, a = butter(n, 0.05)
        zi = lfilter_zi(b, a)
        z, _ = lfilter(b, a, xn, zi = zi * xn[0])
        z2, _ = lfilter(b, a, z, zi = zi * z[0])
        y = filtfilt(b, a, xn)
        
        return z, z2, y
    
    def visualization(self, signal: np.ndarray, z, z2, y, title: str):
        """
        Visualize the returned parameters of digital_filter function.
        """
        plt.figure
        plt.plot(signal, 'b', alpha = 0.75)
        plt.plot(z, 'r--', z2, 'r', y, 'k')
        plt.legend(('noisy signal', 'lfilter, once', 'lfilter, twice',
            'filtfilt'), loc = 'best')
        plt.title(title)
        plt.xlabel('Timestamp')
        plt.ylabel('coords')
        plt.grid(True)
        plt.show()
    
    def visualize_local_max_min(self, filtfilt: np.ndarray, name: str):
        """
        Visualize filtfilt filtered signal, that one with linear phase.
        """
        df = pd.DataFrame(filtfilt, columns = ['filtfilt'])
        df['min'] = df.iloc[argrelextrema(df.filtfilt.values, np.less_equal,
                    order=3)[0]]['filtfilt']
        df['max'] = df.iloc[argrelextrema(df.filtfilt.values, np.greater_equal,
                    order=3)[0]]['filtfilt']

        plt.scatter(df.index, df['min'], c='r')
        plt.scatter(df.index, df['max'], c='g')
        plt.title('filtfilt: ' + name)
        plt.xlabel('Timestamp')
        plt.ylabel('coords')
        plt.plot(df.index, df['filtfilt'])
        plt.show()
