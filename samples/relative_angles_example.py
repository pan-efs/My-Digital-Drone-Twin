import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import argrelextrema
from biomechanics.biomechanics2D import AngularKinematics as AngularKinematics
from biomechanics.biomechanics2D import LinearKinematics as LinearKinematics

#
# General: Calculate and visualize knee biomechanics parameters. Input is a .txt file.
#

# Into text file there are the 2D coordinates of lower body.
file_path = 'C:\\Users\\Drone\\Desktop\\Panagiotis\\My-Digital-Drone-Twin\\samples\\lower_body_example.txt'

# Convert .txt to dataframe
df = pd.read_csv(file_path, delimiter = ",", header = None)
# Rename columns
df = df.rename({0: 'time', 1: 'hip_r_x', 2: 'hip_r_y', 3: 'knee_r_x', 4: 'knee_r_y', 5: 'ankle_r_x', 6: 'ankle_r_y',
                7: 'hip_l_x', 8: 'hip_l_y', 9: 'knee_l_x', 10: 'knee_l_y', 11: 'ankle_l_x', 12: 'ankle_l_y'},
                axis = 'columns')

# Split dataframe
time = df.loc[0:103, 'time']

hip_right = df.loc[0:103, 'hip_r_x':'hip_r_y']
knee_right = df.loc[0:103, 'knee_r_x':'knee_r_y']
ankle_right = df.loc[0:103, 'ankle_r_x':'ankle_r_y']

hip_left = df.loc[0:103, 'hip_l_x':'hip_l_y']
knee_left = df.loc[0:103, 'knee_l_x':'knee_l_y']
ankle_left = df.loc[0:103, 'ankle_l_x':'ankle_l_y']

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
time1 = time.drop(time.index[103])

# Visualisation of knee angles
fig, (ax1, ax2) = plt.subplots(1,2)
ax1.plot(time1, r_theta)
ax1.set_title('Knee angle (Right)')
ax1.set(xlabel = 'Time (s)', ylabel = 'Knee angle (degrees)')

ax2.plot(time1, l_theta)
ax2.set_title('Knee angle (Left)')
ax2.set(xlabel = 'Time (s)', ylabel = 'Knee angle (degrees)')

# First figure
plt.show()

# Find local min and max values
df1 = pd.DataFrame(r_theta, columns = ['r_knee'])
df1['min'] = df1.iloc[argrelextrema(df1.r_knee.values, np.less_equal,
                    order=5)[0]]['r_knee']
df1['max'] = df1.iloc[argrelextrema(df1.r_knee.values, np.greater_equal,
                    order=5)[0]]['r_knee']

df2 = pd.DataFrame(l_theta, columns = ['l_knee'])
df2['min'] = df2.iloc[argrelextrema(df2.l_knee.values, np.less_equal,
                    order=5)[0]]['l_knee']
df2['max'] = df2.iloc[argrelextrema(df2.l_knee.values, np.greater_equal,
                    order=5)[0]]['l_knee']

fig1, (ax3, ax4) = plt.subplots(1,2)
ax3.scatter(df1.index, df1['min'], c='r')
ax3.scatter(df1.index, df1['max'], c='g')
ax3.set_title('Right knee')
ax3.plot(df1.index, df1['r_knee'])

ax4.scatter(df2.index, df2['min'], c='r')
ax4.scatter(df2.index, df2['max'], c='g')
ax4.set_title('Left knee')
ax4.plot(df2.index, df2['l_knee'])

# Second figure
plt.show()

# Calculate velocity of knee joint
vel_knee_right = pd.concat([time, knee_right], axis = 1)
vel_knee_right = vel_knee_right.rename({'knee_r_x': 'joint_x', 'knee_r_y': 'joint_y'}, axis = 'columns')

vel_knee_left = pd.concat([time, knee_left], axis = 1)
vel_knee_left = vel_knee_left.rename({'knee_l_x': 'joint_x', 'knee_l_y': 'joint_y'}, axis = 'columns')

# Create LinearKinematics object
l = LinearKinematics()

# On screen with open VScode a red line appears as error. It's a bug of the editor.
# Calculate velocities vectors for x, y
time_vel_knee_r, velX_knee_r, velY_knee_r = l.calculate_velocity(vel_knee_right)
time_vel_knee_l, velX_knee_l, velY_knee_l = l.calculate_velocity(vel_knee_left)

# Calculate speed
time_speed_knee_r, speed_knee_r = l.calculate_speed(vel_knee_right)
time_speed_knee_l, speed_knee_l = l.calculate_speed(vel_knee_left)

# Visualisation speed, velocity_X and velocity_Y
fig2, (ax5, ax6) = plt.subplots(1,2)
ax5.plot(time_vel_knee_r, velX_knee_r, color = 'b')
ax5.set_title('Knee velocity_X (Right)')
ax5.set(xlabel = 'Time (s)', ylabel = 'Velocity X (m/s)')

ax6.plot(time_vel_knee_r, velY_knee_r, color = 'r')
ax6.set_title('Knee velocity_Y (Right)')
ax6.set(xlabel = 'Time (s)', ylabel = 'Velocity Y (m/s)')

# Third figure
plt.show()

fig3, (ax7, ax8) = plt.subplots(1,2)
ax7.plot(time_vel_knee_l, velX_knee_l, color = 'b')
ax7.set_title('Knee velocity_X (Left)')
ax7.set(xlabel = 'Time (s)', ylabel = 'Velocity X (m/s)')

ax8.plot(time_vel_knee_l, velY_knee_l, color = 'r')
ax8.set_title('Knee velocity_Y (Left)')
ax8.set(xlabel = 'Time (s)', ylabel = 'Velocity Y (m/s)')

# Fourth figure
plt.show()

fig4, (ax9, ax10) = plt.subplots(1,2)
ax9.plot(time_speed_knee_r, speed_knee_r, color = 'b')
ax9.set_title('Knee speed (Right)')
ax9.set(xlabel = 'Time (s)', ylabel = 'Speed (m/s)')

ax10.plot(time_speed_knee_l, speed_knee_l, color = 'r')
ax10.set_title('Knee speed (Left)')
ax10.set(xlabel = 'Time (s)', ylabel = 'Speed (m/s)')

# Fifth figure
plt.show()

# Calculate displacement of x,y components and resultant
time_knee_r_dis, knee_dx_r, knee_dy_r, knee_res_r = l.calculate_displacement(vel_knee_right)
time_knee_l_dis, knee_dx_l, knee_dy_l, knee_res_l = l.calculate_displacement(vel_knee_left)

# Visualize displacement
fig5, (ax11, ax12) = plt.subplots(1,2)
ax11.plot(time_knee_r_dis, knee_res_r, color = 'b')
ax11.set_title('Knee displacement (Right)')
ax11.set(xlabel = 'Time (s)', ylabel = 'Resultant (m)')

ax12.plot(time_knee_l_dis, knee_res_l, color = 'r')
ax12.set_title('Knee displacement (Left)')
ax12.set(xlabel = 'Time (s)', ylabel = 'Resultant (m)')

# Sixth figure
plt.show()
