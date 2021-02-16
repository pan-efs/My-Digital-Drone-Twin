import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import *
from filters.digital_filter import DigitalFilter as DigitalFilter
from biomechanics.biomechanics2D import AngularKinematics as AngularKinematics
from biomechanics.biomechanics2D import LinearKinematics as LinearKinematics

#
# This file contains how we can apply digital filter (IIR or FIR) on a sequence of data.
# Visualizations are included as well. 
#

file_path = 'C:\\Users\\Drone\\Desktop\\Panagiotis\\My-Digital-Drone-Twin\\samples\\data\\flex_back_side.txt'

# Convert .txt to dataframe
df = pd.read_csv(file_path, delimiter = ",", header = None)
# Rename columns
df = df.rename({0: 'time', 1: 'hip_r_x', 2: 'hip_r_y', 3: 'knee_r_x', 4: 'knee_r_y', 5: 'ankle_r_x', 6: 'ankle_r_y',
                7: 'hip_l_x', 8: 'hip_l_y', 9: 'knee_l_x', 10: 'knee_l_y', 11: 'ankle_l_x', 12: 'ankle_l_y'},
                axis = 'columns')

# Split dataframe
time = df.loc[0:(len(df) - 1), 'time']

hip_right = df.loc[0:(len(df) - 1), 'hip_r_x':'hip_r_y']
knee_right = df.loc[0:(len(df) - 1), 'knee_r_x':'knee_r_y']
ankle_right = df.loc[0:(len(df) - 1), 'ankle_r_x':'ankle_r_y']

hip_left = df.loc[0:(len(df) - 1), 'hip_l_x':'hip_l_y']
knee_left = df.loc[0:(len(df) - 1), 'knee_l_x':'knee_l_y']
ankle_left = df.loc[0:(len(df) - 1), 'ankle_l_x':'ankle_l_y']

# Convert dataframe to array
hip_right_array = hip_right.to_numpy()
knee_right_array = knee_right.to_numpy()
ankle_right_array = ankle_right.to_numpy()

hip_left_array = hip_left.to_numpy()
knee_left_array = knee_left.to_numpy()
ankle_left_array = ankle_left.to_numpy()

# Left side of lower body
hipLeftX = []
hipLeftY = []
kneeLeftX = []
kneeLeftY = []
ankleLeftX = []
ankleLeftY = []
for i in range(0, len(hip_left_array)):
    hipLeftX.append(hip_left_array[i][0])
    hipLeftY.append(hip_left_array[i][1])
    
for i in range(0, len(knee_left_array)):
    kneeLeftX.append(knee_left_array[i][0])
    kneeLeftY.append(knee_left_array[i][1])

for i in range(0, len(ankle_left_array)):
    ankleLeftX.append(ankle_left_array[i][0])
    ankleLeftY.append(ankle_left_array[i][1])

# Right side of lower body
hipRightX = []
hipRightY = []
kneeRightX = []
kneeRightY = []
ankleRightX = []
ankleRightY = []
for i in range(0, len(hip_right_array)):
    hipRightX.append(hip_right_array[i][0])
    hipRightY.append(hip_right_array[i][1])

for i in range(0, len(knee_right_array)):
    kneeRightX.append(knee_right_array[i][0])
    kneeRightY.append(knee_right_array[i][1])

for i in range(0, len(ankle_right_array)):
    ankleRightX.append(ankle_right_array[i][0])
    ankleRightY.append(ankle_right_array[i][1])

#
#Filter data along one-dimension with an IIR or FIR filter.
# 

# Create DigitalFilter object
f = DigitalFilter()

# Left side of lower body
# hipLeftX
z, z2, y_hlx = f.digital_filter(hipLeftX, 3)
f.visualization(hipLeftX, z, z2, y_hlx, 'Hip Left X axis')
f.visualize_local_max_min(y_hlx, 'Hip Left X')

# hipLeftY
z, z2, y_hly = f.digital_filter(hipLeftY, 3)
f.visualization(hipLeftY, z, z2, y_hly, 'Hip Left Y axis')
f.visualize_local_max_min(y_hly, 'Hip Left Y')

# kneeLeftX
z, z2, y_klx = f.digital_filter(kneeLeftX, 3)
f.visualization(kneeLeftX, z, z2, y_klx, 'Knee Left X axis')
f.visualize_local_max_min(y_klx, 'Knee Left X')

# kneeLeftY
z, z2, y_kly = f.digital_filter(kneeLeftY, 3)
f.visualization(kneeLeftY, z, z2, y_kly, 'Knee Left Y axis')
f.visualize_local_max_min(y_kly, 'Knee Left Y')

# ankleLeftX
z, z2, y_alx = f.digital_filter(ankleLeftX, 3)
f.visualization(ankleLeftX, z, z2, y_alx, 'Ankle Left X axis')
f.visualize_local_max_min(y_alx, 'Ankle Left X')

# ankleLeftY
z, z2, y_aly = f.digital_filter(ankleLeftY, 3)
f.visualization(ankleLeftY, z, z2, y_aly, 'Ankle Left Y axis')
f.visualize_local_max_min(y_aly, 'Ankle Left Y')

# Right side of lower body
# hipRightX
z, z2, y_hrx = f.digital_filter(hipRightX, 3)
f.visualization(hipRightX, z, z2, y_hrx, 'Hip Right X axis')
f.visualize_local_max_min(y_hrx, 'Hip Right X')

# hipRightY
z, z2, y_hry = f.digital_filter(hipRightY, 3)
f.visualization(hipRightY, z, z2, y_hry, 'Hip Right Y axis')
f.visualize_local_max_min(y_hry, 'Hip Right Y')

# kneeRightX
z, z2, y_krx = f.digital_filter(kneeRightX, 3)
f.visualization(kneeRightX, z, z2, y_krx, 'Knee Right X axis')
f.visualize_local_max_min(y_krx, 'Knee Right X')

# kneeRightY
z, z2, y_kry = f.digital_filter(kneeRightY, 3)
f.visualization(kneeRightY, z, z2, y_kry, 'Knee Right Y axis')
f.visualize_local_max_min(y_kry, 'Knee Right Y')

# ankleRightX
z, z2, y_arx = f.digital_filter(ankleRightX, 3)
f.visualization(ankleRightX, z, z2, y_arx, 'Ankle Right X axis')
f.visualize_local_max_min(y_arx, 'Ankle Right X')

# ankleRightY
z, z2, y_ary = f.digital_filter(ankleRightY, 3)
f.visualization(ankleRightY, z, z2, y_ary, 'Ankle Right Y axis')
f.visualize_local_max_min(y_ary, 'Ankle Right Y')

#-------Biomechanics part-------#

# Convert to 2D arrays as before
hip_left_filtered = np.vstack((y_hlx, y_kly)).T
knee_left_filtered = np.vstack((y_klx, y_kly)).T
ankle_left_filtered = np.vstack((y_alx, y_aly)).T

hip_right_filtered = np.vstack((y_hrx, y_hry)).T
knee_right_filtered = np.vstack((y_krx, y_kry)).T
ankle_right_filtered = np.vstack((y_arx, y_ary)).T

# Create AngularKinematics object
k = AngularKinematics()

# Normalize coordinates according to image height and width
hip_right_filtered_normalized = k.normalize_2d_coordinates(hip_right_filtered, 1280, 720)
knee_right_filtered_normalized = k.normalize_2d_coordinates(knee_right_filtered, 1280, 720)
ankle_right_filtered_normalized = k.normalize_2d_coordinates(ankle_right_filtered, 1280, 720)

hip_left_filtered_normalized = k.normalize_2d_coordinates(hip_left_filtered, 1280, 720)
knee_left_filtered_normalized = k.normalize_2d_coordinates(knee_left_filtered, 1280, 720)
ankle_left_filtered_normalized = k.normalize_2d_coordinates(ankle_left_filtered, 1280, 720)

# Calculate the angles
r_theta = k.calculate_relative_angle(hip_right_filtered_normalized, knee_right_filtered_normalized, ankle_right_filtered_normalized)
l_theta = k.calculate_relative_angle(hip_left_filtered_normalized, knee_left_filtered_normalized, ankle_left_filtered_normalized)

# Drop last row of time for equality reasons
time1 = time.loc[0:(len(df) - 2)]

# Visualisation of knee angles
fig, (ax1, ax2) = plt.subplots(1,2)
ax1.plot(time1, r_theta)
ax1.set_title('Knee angle (Right)')
ax1.set(xlabel = 'Time (s)', ylabel = 'Knee angle (degrees)')

ax2.plot(time1, l_theta)
ax2.set_title('Knee angle (Left)')
ax2.set(xlabel = 'Time (s)', ylabel = 'Knee angle (degrees)')

# Filtered figure
plt.show()