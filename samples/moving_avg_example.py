import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import argrelextrema
from sklearn.metrics import mean_squared_error
from filters.moving_average import MovingAverage as MovingAverage
from biomechanics.biomechanics2D import AngularKinematics as AngularKinematics
from biomechanics.biomechanics2D import LinearKinematics as LinearKinematics

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

# Convert to 2D arrays as before
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

# Estimation of velocities
# Create LinearKinematics object
l = LinearKinematics()

# Call velocity function for each joint separately
time_vel_HR, hip_right_velX, hip_right_velY = l.cal_velocity(time, hip_right_filtered)
time_vel_HL, hip_left_velX, hip_left_velY = l.cal_velocity(time, hip_left_filtered)
time_vel_KR, knee_right_velX, knee_right_velY = l.cal_velocity(time, knee_right_filtered)
time_vel_KL, knee_left_velX, knee_left_velY = l.cal_velocity(time, knee_left_filtered)
time_vel_AR, ankle_right_velX, ankle_right_velY = l.cal_velocity(time, ankle_right_filtered)
time_vel_AL, ankle_left_velX, ankle_left_velY = l.cal_velocity(time, ankle_left_filtered)

# Visualizations of velocities
fig2, (ax5, ax6) = plt.subplots(1,2)
ax5.plot(time_vel_HL, hip_left_velX, c = 'r')
ax5.set(xlabel = 'Time (s)', ylabel = 'Velocity X (m\s)')
ax5.set_title('Hip left')

ax6.plot(time_vel_HL, hip_left_velY, c = 'b')
ax6.set(xlabel = 'Time (s)', ylabel = 'Velocity Y (m\s)')
ax6.set_title('Hip left')

plt.show()

fig3, (ax7, ax8) = plt.subplots(1,2)
ax7.plot(time_vel_KL, knee_left_velX, c = 'r')
ax7.set(xlabel = 'Time (s)', ylabel = 'Velocity X (m\s)')
ax7.set_title('Knee left')

ax8.plot(time_vel_KL, knee_left_velY, c = 'b')
ax8.set(xlabel = 'Time (s)', ylabel = 'Velocity Y (m\s)')
ax8.set_title('Knee left')

plt.show()

fig4, (ax9, ax10) = plt.subplots(1,2)
ax9.plot(time_vel_AL, ankle_left_velX, c = 'r')
ax9.set(xlabel = 'Time (s)', ylabel = 'Velocity X (m\s)')
ax9.set_title('Ankle left')

ax10.plot(time_vel_AL, ankle_left_velY, c = 'b')
ax10.set(xlabel = 'Time (s)', ylabel = 'Velocity Y (m\s)')
ax10.set_title('Ankle left')

plt.show()

# Estimation of accelerations

# Convert velocities to 2D arrays
hip_right_vel = np.vstack((hip_right_velX, hip_right_velY)).T
hip_left_vel = np.vstack((hip_left_velX, hip_left_velY)).T
knee_right_vel = np.vstack((knee_right_velX, knee_right_velY)).T
knee_left_vel = np.vstack((knee_left_velX, knee_left_velY)).T
ankle_right_vel = np.vstack((ankle_right_velX, ankle_right_velY)).T
ankle_left_vel = np.vstack((ankle_left_velX, ankle_left_velY)).T

# Call acceleration function for each joint separately
time_acc_HR, hip_right_accX, hip_right_accY = l.cal_acceleration(time_vel_HR, hip_right_vel)
time_acc_HL, hip_left_accX, hip_left_accY = l.cal_acceleration(time_vel_HL, hip_left_vel)
time_acc_KR, knee_right_accX, knee_right_accY = l.cal_acceleration(time_vel_KR, knee_right_vel)
time_acc_KL, knee_left_accX, knee_left_accY = l.cal_acceleration(time_vel_KL, knee_left_vel)
time_acc_AR, ankle_right_accX, ankle_right_accY = l.cal_acceleration(time_vel_AR, ankle_right_vel)
time_acc_AL, ankle_left_accX, ankle_left_accY = l.cal_acceleration(time_vel_AL, ankle_left_vel)

# Visualizations of accelerations
fig5, (ax11, ax12) = plt.subplots(1,2)
ax11.plot(time_acc_HL, hip_left_accX, c = 'r')
ax11.set(xlabel = 'Time (s)', ylabel = 'Acceleration X (m\s^2)')
ax11.set_title('Hip left')

ax12.plot(time_acc_HL, hip_left_accY, c = 'b')
ax12.set(xlabel = 'Time (s)', ylabel = 'Acceleration Y (m\s^2)')
ax12.set_title('Hip left')

plt.show()

fig6, (ax13, ax14) = plt.subplots(1,2)
ax13.plot(time_acc_KL, knee_left_accX, c = 'r')
ax13.set(xlabel = 'Time (s)', ylabel = 'Acceleration X (m\s^2)')
ax13.set_title('Knee left')

ax14.plot(time_acc_KL, knee_left_accY, c = 'b')
ax14.set(xlabel = 'Time (s)', ylabel = 'Acceleration Y (m\s^2)')
ax14.set_title('Knee left')

plt.show()

fig7, (ax15, ax16) = plt.subplots(1,2)
ax15.plot(time_acc_AL, ankle_left_accX, c = 'r')
ax15.set(xlabel = 'Time (s)', ylabel = 'Acceleration X (m\s^2)')
ax15.set_title('Ankle left')

ax16.plot(time_acc_AL, ankle_left_accY, c = 'b')
ax16.set(xlabel = 'Time (s)', ylabel = 'Acceleration Y (m\s^2)')
ax16.set_title('Ankle left')

plt.show()