from filterpy.kalman import KalmanFilter
from filterpy.common import Q_discrete_white_noise
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class Kalman_filters:
    def __init__(self):
        pass
    
    def smoothing_filter(self, data: np.ndarray):
        fk = KalmanFilter(dim_x=2, dim_z=1)
        fk.x = np.array([0., 1.])      # state (x and dx)
        fk.F = np.array([[1., 1.],
                        [0., 1.]])    # state transition matrix
        fk.H = np.array([[1., 0.]])    # Measurement function
        fk.P*= 10.                     # covariance matrix
        fk.R = 25                   # state uncertainty
        fk.Q = Q_discrete_white_noise(dim=2, dt=1., var=0.001)  # process uncertainty
        
        mu, cov, _, _ = fk.batch_filter(data)
        M, P, C, _ = fk.rts_smoother(mu, cov)
        
        return M, mu

    def visualization(self, data: np.ndarray, M, mu, title: str):
        plt.plot(data, c = 'r', label = 'Measurements')
        plt.plot(M[:, 0], c = 'b', label = 'RTS')
        plt.plot(mu[:, 0], c = 'g', ls = '--', label = 'KF Output')
        plt.title(title)
        plt.xlabel('Frames')
        plt.ylabel('Degrees')
        plt.legend(loc = 3)
        plt.show()
    
    def double_visualization(self, r_kf_data: np.ndarray, r_rts_data: np.ndarray,
                            l_kf_data: np.ndarray, l_rts_data: np.ndarray,
                            r_title: str, l_title: str):
        fig, (ax1, ax2) = plt.subplots(1,2)
        ax1.plot(r_kf_data, c = 'g', ls = '--', label = 'KF Output')
        ax1.plot(r_rts_data, c = 'b', label = 'RTS')
        ax1.set_title(r_title)
        ax1.set(xlabel = 'Frames', ylabel = 'Knee angle (degrees)')
        
        ax2.plot(l_kf_data, c = 'g', ls = '--', label = 'KF Output')
        ax2.plot(l_rts_data, c = 'b', label = 'RTS')
        ax2.set_title(l_title)
        ax2.set(xlabel = 'Frames', ylabel = 'Knee angle (degrees)')
        
        plt.legend(loc = 4)
        plt.show()