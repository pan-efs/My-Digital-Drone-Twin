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
    

# TODO: Does not run in 'samples' folder, so I leave it here as well.
# Example of how we can analyse our data before we feed it to kalman filter.
# We should filter each joint. However, occlusions prone to errors and performance loss.
# Revise kalman filter and its implementation. 

joint_type_path = 'C:/Users/user/Desktop/KTH/Master Thesis/Logs cpp/joint_type.txt'
position_x_path = 'C:/Users/user/Desktop/KTH/Master Thesis/Logs cpp/position_X.txt'
position_y_path = 'C:/Users/user/Desktop/KTH/Master Thesis/Logs cpp/position_Y.txt'
position_z_path = 'C:/Users/user/Desktop/KTH/Master Thesis/Logs cpp/position_Z.txt'
proj_x_path = 'C:/Users/user/Desktop/KTH/Master Thesis/Logs cpp/projectile_X.txt'
proj_y_path = 'C:/Users/user/Desktop/KTH/Master Thesis/Logs cpp/projectile_Y.txt'
proj_z_path = 'C:/Users/user/Desktop/KTH/Master Thesis/Logs cpp/projectile_Z.txt'

".txt to df"
df1 = pd.read_csv(joint_type_path, delimiter = ",", header = None)
df2 = pd.read_csv(position_x_path, delimiter = ",", header = None)
df3 = pd.read_csv(position_y_path, delimiter = ",", header = None)
df4 = pd.read_csv(position_z_path, delimiter = ",", header = None)
df5 = pd.read_csv(proj_x_path, delimiter = ",", header = None)
df6 = pd.read_csv(proj_y_path, delimiter = ",", header = None)
df7 = pd.read_csv(proj_z_path, delimiter = ",", header = None)

"Transposes"
df1 = df1.T
df2 = df2.T
df3 = df3.T
df4 = df4.T
df5 = df5.T
df6 = df6.T
df7 = df7.T

"concat them into one"
df_pos = pd.concat([df1, df2, df3, df4], ignore_index = True, axis = 1)
df_pos = df_pos.rename({0: 'joint_type', 1: 'pos_x', 2: 'pos_y', 3: 'pos_z'}, 
            axis = 'columns')

df_proj = pd.concat([df1, df5, df6, df7], ignore_index = True, axis = 1)
df_proj = df_proj.rename({0: 'joint_type', 1: '_x', 2: '_y', 3: '_z'}, 
            axis = 'columns')

"sort by joint type"
df_pos = df_pos.sort_values(by = ['joint_type'])
df_proj = df_proj.sort_values(by = ['joint_type'])

"extract desired rows, convert to array, remove joint type, ready for filter!"
LEFT_WRIST = df_pos.loc[df_pos['joint_type'] == 8]
LEFT_WRIST = LEFT_WRIST.to_numpy()
LEFT_WRIST = np.delete(LEFT_WRIST, np.s_[0], 1)

k = kalmanFilter()
k.visualisation(LEFT_WRIST)