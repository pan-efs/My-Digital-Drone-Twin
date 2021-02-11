import pandas as pd
import numpy as np
from kalman_filter.kalmanFilter import kalmanFilter as kalmanFilter

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