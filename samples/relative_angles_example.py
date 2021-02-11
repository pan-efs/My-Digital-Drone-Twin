import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import argrelextrema
from biomechanics.biomechanics2D import AngularKinematics as AngularKinematics

#
# General: Calculate knee relative angles from a text file.
#

# Into text file there are the 2D coordinates of lower body.
file_path = 'C:\\Users\\Drone\\Desktop\\Panagiotis\\My-Digital-Drone-Twin\\cubemos\\lower_body_example.txt'

# Convert .txt to dataframe
df = pd.read_csv(file_path, delimiter = ",", header = None)
# Rename columns
df = df.rename({0: 'time', 1: 'hip_r_x', 2: 'hip_r_y', 3: 'knee_r_x', 4: 'knee_r_y', 5: 'ankle_r_x', 6: 'ankle_r_y',
                7: 'hip_l_x', 8: 'hip_l_y', 9: 'knee_l_x', 10: 'knee_l_y', 11: 'ankle_l_x', 12: 'ankle_l_y'},
                axis = 'columns')

# Split dataframe
time = df.loc[0:60, 'time']

hip_right = df.loc[0:60, 'hip_r_x':'hip_r_y']
knee_right = df.loc[0:60, 'knee_r_x':'knee_r_y']
ankle_right = df.loc[0:60, 'ankle_r_x':'ankle_r_y']

hip_left = df.loc[0:60, 'hip_l_x':'hip_l_y']
knee_left = df.loc[0:60, 'knee_l_x':'knee_l_y']
ankle_left = df.loc[0:60, 'ankle_l_x':'ankle_l_y']

# Convert dataframe to array
hip_right_array = hip_right.to_numpy()
knee_right_array = knee_right.to_numpy()
ankle_right_array = ankle_right.to_numpy()

hip_left_array = hip_left.to_numpy()

knee_left_array = knee_left.to_numpy()
ankle_left_array = ankle_left.to_numpy()

# Create AngularKinematics object
k = AngularKinematics()

# Normalize coordinates according to image height and width
hip_right_array = k.normalize_2d_coordinates(hip_right_array, 1280, 720)
knee_right_array = k.normalize_2d_coordinates(knee_right_array, 1280, 720)
ankle_right_array = k.normalize_2d_coordinates(ankle_right_array, 1280, 720)

hip_left_array = k.normalize_2d_coordinates(hip_left_array, 1280, 720)
knee_left_array = k.normalize_2d_coordinates(knee_left_array, 1280, 720)
ankle_left_array = k.normalize_2d_coordinates(ankle_left_array, 1280, 720)

# Calculate the angles
r_theta = k.calculate_relative_angle(hip_right_array, knee_right_array, ankle_right_array)
l_theta = k.calculate_relative_angle(hip_left_array, knee_left_array, ankle_left_array)

# print theta array
#print(r_theta)
#print(l_theta)

# Drop last row of time for equality reasons
time = time.drop(time.index[60])

# Visualisation of knee angles
fig, (ax1, ax2) = plt.subplots(1,2)
ax1.plot(time, r_theta)
ax1.set_title('Knee angle (Right)')
ax1.set(xlabel = 'Time (ms)', ylabel = 'Knee angle (degrees)')

ax2.plot(time, l_theta)
ax2.set_title('Knee angle (Left)')
ax2.set(xlabel = 'Time (ms)', ylabel = 'Knee angle (degrees)')

plt.show()

# Find local min and max values
df1 = pd.DataFrame(r_theta, columns = ['r_knee'])
df1['min'] = df1.iloc[argrelextrema(df1.r_knee.values, np.less_equal,
                    order=3)[0]]['r_knee']
df1['max'] = df1.iloc[argrelextrema(df1.r_knee.values, np.greater_equal,
                    order=3)[0]]['r_knee']

df2 = pd.DataFrame(l_theta, columns = ['l_knee'])
df2['min'] = df2.iloc[argrelextrema(df2.l_knee.values, np.less_equal,
                    order=3)[0]]['l_knee']
df2['max'] = df2.iloc[argrelextrema(df2.l_knee.values, np.greater_equal,
                    order=3)[0]]['l_knee']

fig1, (ax1, ax2) = plt.subplots(1,2)
ax1.scatter(df1.index, df1['min'], c='r')
ax1.scatter(df1.index, df1['max'], c='g')
ax1.set_title('Right knee')
ax1.plot(df1.index, df1['r_knee'])

ax2.scatter(df2.index, df2['min'], c='r')
ax2.scatter(df2.index, df2['max'], c='g')
ax2.set_title('Left knee')
ax2.plot(df2.index, df2['l_knee'])

plt.show()


