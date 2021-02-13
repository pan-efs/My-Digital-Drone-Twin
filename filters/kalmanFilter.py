from pykalman import KalmanFilter
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class kalmanFilter:
    
    """
    Description: [text]:
    Kalman filter and Kalman smoother in order to "denoise" our skeleton data for each joint.
    
    Parameters: [array]: [an array of observations]
    """
    def kalman_filter(self, measurements: np.array):
        "μ"
        initial_state_mean = [0,0,0]
        
        "A"
        transition_matrix = [[1, 0, 0],
                            [0, 1, 0],
                            [0, 0, 1]]
        
        "Η"
        observation_matrix = [[1, 0, 0],
                            [0, 1, 0],
                            [0, 0, 1]]
        
        "filter"
        kf = KalmanFilter(transition_matrices = transition_matrix,
                        observation_matrices = observation_matrix,
                        initial_state_mean = initial_state_mean)
        
        "smooth"
        kf = kf.em(measurements, n_iter = 5)
        (smoothed_state_means, smoothed_state_covariances) = kf.smooth(measurements)
        
        kf1 = KalmanFilter(transition_matrices = transition_matrix,
                        observation_matrices = observation_matrix,
                        initial_state_mean = initial_state_mean,
                        observation_covariance = 10*kf.observation_covariance,
                        em_vars = ['transition_covariance', 'initial_state_covariance'])
        "smooth"
        kf1 = kf1.em(measurements, n_iter = 5)
        (smoothed_state_means, smoothed_state_covariances) = kf1.smooth(measurements)
        
        return smoothed_state_means
    
    """
    Description: [text]:
    Plot real observation data against filtered data.
    
    Parameters: [array]: [an array of observations]
    
    Returns: [figure]: [plot data] 
    """
    def visualisation(self, measurements: np.array):
        smoothed_state_means = self.kalman_filter(measurements)
        
        plt.figure(1)
        
        times = range(measurements.shape[0])
        
        plt.plot(times, measurements[:, 0], 'bo',
                times, measurements[:, 1], 'ro',
                times, measurements[:, 2], 'go',
                times, smoothed_state_means[:, 0], 'b--',
                times, smoothed_state_means[:, 1], 'r--',
                times, smoothed_state_means[:, 2], 'g--')
        
        plt.show()
    
    """
    Description: [text]:
    Convert a text file into array.
    
    Parameters: [file]: [.txt]
    
    Returns: [array]: [numpy array]
    """
    def convert_text_to_array(self, file: str):
        x, y, z = np.loadtxt(file, delimiter = ',', usecols = (1, 2, 3), unpack = True)
        return x, y, z
