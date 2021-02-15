import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import *
from filters.digital_filter import DigitalFilter as DigitalFilter

#
# This file contains how we can apply digital filter (IIR or FIR) on a sequence of data.
# Visualizations are included as well. 
#


file_path = 'C:\\Users\\Drone\\Desktop\\Panagiotis\\My-Digital-Drone-Twin\\samples\\LK_flexion_extension.txt'

# Convert .txt to dataframe
df = pd.read_csv(file_path, delimiter = ",", header = None)
# Rename columns
df = df.rename({0: 'time', 1: 'hip_r_x', 2: 'hip_r_y', 3: 'knee_r_x', 4: 'knee_r_y', 5: 'ankle_r_x', 6: 'ankle_r_y',
                7: 'hip_l_x', 8: 'hip_l_y', 9: 'knee_l_x', 10: 'knee_l_y', 11: 'ankle_l_x', 12: 'ankle_l_y'},
                axis = 'columns')

# Split dataframe
time = df.loc[0:192, 'time']

hip_right = df.loc[0:192, 'hip_r_x':'hip_r_y']
knee_right = df.loc[0:192, 'knee_r_x':'knee_r_y']
ankle_right = df.loc[0:192, 'ankle_r_x':'ankle_r_y']

hip_left = df.loc[0:192, 'hip_l_x':'hip_l_y']
knee_left = df.loc[0:192, 'knee_l_x':'knee_l_y']
ankle_left = df.loc[0:192, 'ankle_l_x':'ankle_l_y']

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

# kneeLeftX
z, z2, y = f.digital_filter(kneeLeftX, 3)
f.visualization(kneeLeftX, z, z2, y, 'Knee Left X axis')
f.visualize_local_max_min(y, 'Knee Left X')

# kneeLeftY
z, z2, y = f.digital_filter(kneeLeftY, 3)
f.visualization(kneeLeftY, z, z2, y, 'Knee Left Y axis')
f.visualize_local_max_min(y, 'Knee Left Y')

# ankleLeftX
z, z2, y = f.digital_filter(ankleLeftX, 3)
f.visualization(ankleLeftX, z, z2, y, 'Ankle Left X axis')
f.visualize_local_max_min(y, 'Ankle Left X')

# ankleLeftY
z, z2, y = f.digital_filter(ankleLeftY, 3)
f.visualization(ankleLeftY, z, z2, y, 'Ankle Left Y axis')
f.visualize_local_max_min(y, 'Ankle Left Y')