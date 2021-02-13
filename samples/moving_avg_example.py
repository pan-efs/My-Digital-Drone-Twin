import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import argrelextrema
from sklearn.metrics import mean_squared_error
from filters.moving_average import MovingAverage as MovingAverage
from biomechanics.biomechanics2D import AngularKinematics as AngularKinematics

file_path = 'C:\\Users\\Drone\\Desktop\\Panagiotis\\My-Digital-Drone-Twin\\samples\\LK_flexion_extension.txt'

# Convert .txt to dataframe
df = pd.read_csv(file_path, delimiter = ",", header = None)
# Rename columns
df = df.rename({0: 'time', 1: 'hip_r_x', 2: 'hip_r_y', 3: 'knee_r_x', 4: 'knee_r_y', 5: 'ankle_r_x', 6: 'ankle_r_y',
                7: 'hip_l_x', 8: 'hip_l_y', 9: 'knee_l_x', 10: 'knee_l_y', 11: 'ankle_l_x', 12: 'ankle_l_y'},
                axis = 'columns')

# Split dataframe # 103
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

# Create MovingAverage object
p = MovingAverage()

# Apply moving average filter
hX = p.moving_average(hipLeftX, 3)
hY = p.moving_average(hipLeftY, 3)
mX = p.moving_average(kneeLeftX, 3)
mY = p.moving_average(kneeLeftY, 3)
eX = p.moving_average(ankleLeftX, 3)
eY = p.moving_average(ankleLeftY, 3)

jX = p.moving_average(hipRightX, 3)
jY = p.moving_average(hipRightY, 3)
kX = p.moving_average(kneeRightX, 3)
kY = p.moving_average(kneeRightY, 3)
aX = p.moving_average(ankleRightX, 3)
aY = p.moving_average(ankleRightY, 3)

# Convert two 2D array as before
hip_left_filtered = np.vstack((hX, hY)).T
knee_left_filtered = np.vstack((mX, mY)).T
ankle_left_filtered = np.vstack((eX, eY)).T

hip_right_filtered = np.vstack((jX, jY)).T
knee_right_filtered = np.vstack((kX, kY)).T
ankle_right_filtered = np.vstack((aX, aY)).T

# Drop the last two rows as useless and visualization reasons
hipLeftX = hipLeftX[:len(hipLeftX) - 2]
hipLeftY = hipLeftY[:len(hipLeftY) - 2]
kneeLeftX = kneeLeftX[:len(kneeLeftX) - 2]
kneeLeftY = kneeLeftY[:len(kneeLeftY) - 2]
ankleLeftX = ankleLeftX[:len(ankleLeftX) - 2]
ankleLeftY = ankleLeftY[:len(ankleLeftY) - 2]

hipRightX = hipRightX[:len(hipRightX) - 2]
hipRightY = hipRightY[:len(hipRightY) - 2]
kneeRightX = kneeRightX[:len(kneeRightX) - 2]
kneeRightY = kneeRightY[:len(kneeRightY) - 2]
ankleRightX = ankleRightX[:len(ankleRightX) - 2]
ankleRightY = ankleRightY[:len(ankleRightY) - 2]

# Mean squared errors
# Evaluation metric: Mean Per Joint Position Error (MPJPE)
# We don't have ground truth values e.g. from biomechanics lab.

# Left side
error_HLX = mean_squared_error(hipLeftX, hX)
error_HLY = mean_squared_error(hipLeftY, hY)
error_KLX = mean_squared_error(kneeLeftX, mX)
error_KLY = mean_squared_error(kneeLeftY, mY)
error_ALX = mean_squared_error(ankleLeftX, eX)
error_ALY = mean_squared_error(ankleLeftY, eY)

# Right side
error_HRX = mean_squared_error(hipRightX, jX)
error_HRY = mean_squared_error(hipRightY, jY)
error_KRX = mean_squared_error(kneeRightX, kX)
error_KRY = mean_squared_error(kneeRightY, kY)
error_ARX = mean_squared_error(ankleRightX, aX)
error_ARY = mean_squared_error(ankleRightY, aY)

# Save errors
errors = []
errors.append([error_HLX, error_HLY, error_KLX, error_KLY, error_ALX, error_ALY,
                error_HRX, error_HRY, error_KRX, error_KRY, error_ARX, error_ARY])

# A few visualizations to show how moving average looks
plt.plot(kneeLeftX)
plt.plot(mX)
plt.xlabel('Time')
plt.ylabel('x')
plt.title('Knee left')
plt.show()

plt.plot(kneeLeftY)
plt.plot(mY)
plt.xlabel('Time')
plt.ylabel('y')
plt.title('Knee left')
plt.show()

plt.plot(ankleRightX)
plt.plot(aX)
plt.xlabel('Time')
plt.ylabel('x')
plt.title('Ankle right')
plt.show()

plt.plot(ankleRightY)
plt.plot(aY)
plt.xlabel('Time')
plt.ylabel('y')
plt.title('Ankle right')
plt.show()

# Calculate knee angles using the filtered data
# Create AngularKinematics object
k = AngularKinematics()

# Normalize coordinates according to image height and width
hip_right_filtered = k.normalize_2d_coordinates(hip_right_filtered, 1280, 720)
knee_right_filtered = k.normalize_2d_coordinates(knee_right_filtered, 1280, 720)
ankle_right_filtered = k.normalize_2d_coordinates(ankle_right_filtered, 1280, 720)

hip_left_filtered = k.normalize_2d_coordinates(hip_left_filtered, 1280, 720)
knee_left_filtered = k.normalize_2d_coordinates(knee_left_filtered, 1280, 720)
ankle_left_filtered = k.normalize_2d_coordinates(ankle_left_filtered, 1280, 720)

# Calculate the angles
r_theta = k.calculate_relative_angle(hip_right_filtered, knee_right_filtered, ankle_right_filtered)
l_theta = k.calculate_relative_angle(hip_left_filtered, knee_left_filtered, ankle_left_filtered)

# Drop last row of time for equality reasons
time1 = time.loc[0:189]

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

# Show
plt.show()