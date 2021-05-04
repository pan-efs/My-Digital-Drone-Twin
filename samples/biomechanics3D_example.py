import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from animations.anime import Animations
from biomechanics.biomechanics3D import LinearKinematics as LinearKinematics
from biomechanics.biomechanics3D import AngularKinematics as AngularKinematics
from filters.digital_filter import DigitalFilter as DigitalFilter
from filters.kalmanFilter import KalmanFilters as KalmanFilters
from stats.utils_stats import Stats_utils as stats_utils
from sklearn.metrics import mean_squared_error, mean_absolute_error
import os

#--------START FILE--------#

# Define the desired paths here
file_path = 'C:\\Users\\Drone\\Desktop\\Panagiotis\\My-Digital-Drone-Twin\\samples\\data\\rec_pef_cyc_45left_both.txt'
out_path = 'C:\\Users\\Drone\\Desktop\\Panagiotis\\My-Digital-Drone-Twin\\samples\\data\\clean_3d_joints.txt'

#--------END FILE--------#

#--------START HELPER FUNCTIONS--------#

# Helper function to clean the text file from brackets
def remove_brackets(text_file_path):
    fin = open(text_file_path, "rt")
    fout = open(out_path, "wt")
    
    for ln in fin:
        fout.write(ln.replace('[', '').replace(']', ''))
    
    fin.close()
    fout.close()

# Call helper function
remove_brackets(file_path)

# Helper function returning the same length among arrays
def get_same_length(arr1, arr2, arr3):
    len1 = len(arr1)
    len2 = len(arr2)
    len3 = len(arr3)
    min_len = min(len1, len2, len3)
    
    arr1 = arr1[:min_len]
    arr2 = arr2[:min_len]
    arr3 = arr3[:min_len]
    return arr1, arr2, arr3

#--------END HELPER FUNCTIONS--------#

#--------START DATAFRAME PROCESSING--------#

# Convert .txt to dataframe
df = pd.read_csv(out_path, delimiter = ",", header = None)

# Rename columns
df = df.rename({0: 'joint_index', 1: 'joint_x', 2: 'joint_y', 3: 'joint_z'},
                axis = 'columns')

# Split dataframe according to joint_index
joint_0 = df.loc[df['joint_index'] == 0] # nose
joint_1 = df.loc[df['joint_index'] == 1] # upper sternum
joint_2 = df.loc[df['joint_index'] == 2] # upper body
joint_3 = df.loc[df['joint_index'] == 3] # .
joint_4 = df.loc[df['joint_index'] == 4] # .
joint_5 = df.loc[df['joint_index'] == 5] # .
joint_6 = df.loc[df['joint_index'] == 6] # .
joint_7 = df.loc[df['joint_index'] == 7] # .
joint_8 = df.loc[df['joint_index'] == 8] # lower body
joint_9 = df.loc[df['joint_index'] == 9] # .
joint_10 = df.loc[df['joint_index'] == 10] # .
joint_11 = df.loc[df['joint_index'] == 11] # .
joint_12 = df.loc[df['joint_index'] == 12] # .
joint_13 = df.loc[df['joint_index'] == 13] #. 
joint_14 = df.loc[df['joint_index'] == 14] # eyes
joint_15 = df.loc[df['joint_index'] == 15] # .
joint_16 = df.loc[df['joint_index'] == 16] # ears
joint_17 = df.loc[df['joint_index'] == 17] #. 

# Delete joint_index column as unnecessary
del joint_0['joint_index']
del joint_1['joint_index']
del joint_2['joint_index']
del joint_3['joint_index']
del joint_4['joint_index']
del joint_5['joint_index']
del joint_6['joint_index']
del joint_7['joint_index']
del joint_8['joint_index']
del joint_9['joint_index']
del joint_10['joint_index']
del joint_11['joint_index']
del joint_12['joint_index']
del joint_13['joint_index']
del joint_14['joint_index']
del joint_15['joint_index']
del joint_16['joint_index']
del joint_17['joint_index']

# Reset indexes
joint_0 = joint_0.reset_index(drop=True)
joint_1 = joint_1.reset_index(drop=True)
joint_2 = joint_2.reset_index(drop=True)
joint_3 = joint_3.reset_index(drop=True)
joint_4 = joint_4.reset_index(drop=True)
joint_5 = joint_5.reset_index(drop=True)
joint_6 = joint_6.reset_index(drop=True)
joint_7 = joint_7.reset_index(drop=True)
joint_8 = joint_8.reset_index(drop=True)
joint_9 = joint_9.reset_index(drop=True)
joint_10 = joint_10.reset_index(drop=True)
joint_11 = joint_11.reset_index(drop=True)
joint_12 = joint_12.reset_index(drop=True)
joint_13 = joint_13.reset_index(drop=True)
joint_14 = joint_14.reset_index(drop=True)
joint_15 = joint_15.reset_index(drop=True)
joint_16 = joint_16.reset_index(drop=True)
joint_17 = joint_17.reset_index(drop=True)

#--------END DATAFRAME PROCESSING--------#

#--------START CREATE OBJECTS--------#

# Create biomechanics3D objects
k = LinearKinematics()
a = AngularKinematics()

# Create filters objects
f = DigitalFilter()
fil = KalmanFilters()

# Statistics
stats = stats_utils()

#--------END CREATE OBJECTS--------#

#--------START FILTERING--------#

# This technique is repeated for each joint
# Right hip
arr_8x = joint_8['joint_x'].to_numpy()
arr_8y = joint_8['joint_y'].to_numpy()
arr_8z = joint_8['joint_z'].to_numpy()

# BW
z8x, z2_8x, y8x = f.digital_filter(arr_8x, 3)
z8y, z2_8y, y8y = f.digital_filter(arr_8y, 3)
z8z, z2_8z, y8z = f.digital_filter(arr_8z, 3)
# KF, RTS
M8x, mu8x = fil.smoothing_filter(arr_8x)
M8y, mu8y = fil.smoothing_filter(arr_8y)
M8z, mu8z = fil.smoothing_filter(arr_8z) 

# Right knee
arr_9x = joint_9['joint_x'].to_numpy()
arr_9y = joint_9['joint_y'].to_numpy()
arr_9z = joint_9['joint_z'].to_numpy()

# BW
z9x, z2_9x, y9x = f.digital_filter(arr_9x, 3)
z9y, z2_9y, y9y = f.digital_filter(arr_9y, 3)
z9z, z2_9z, y9z = f.digital_filter(arr_9z, 3)
# KF, RTS
M9x, mu9x = fil.smoothing_filter(arr_9x)
M9y, mu9y = fil.smoothing_filter(arr_9y)
M9z, mu9z = fil.smoothing_filter(arr_9z)

# Right ankle
arr_10x = joint_10['joint_x'].to_numpy()
arr_10y = joint_10['joint_y'].to_numpy()
arr_10z = joint_10['joint_z'].to_numpy()

# BW
z10x, z2_10x, y10x = f.digital_filter(arr_10x, 3)
z10y, z2_10y, y10y = f.digital_filter(arr_10y, 3)
z10z, z2_10z, y10z = f.digital_filter(arr_10z, 3)
# KF, RTS
M10x, mu10x = fil.smoothing_filter(arr_10x)
M10y, mu10y = fil.smoothing_filter(arr_10y)
M10z, mu10z = fil.smoothing_filter(arr_10z)

# Left hip
arr_11x = joint_11['joint_x'].to_numpy()
arr_11y = joint_11['joint_y'].to_numpy()
arr_11z = joint_11['joint_z'].to_numpy()

#BW
z11x, z2_11x, y11x = f.digital_filter(arr_11x, 3)
z11y, z2_11y, y11y = f.digital_filter(arr_11y, 3)
z11z, z2_11z, y11z = f.digital_filter(arr_11z, 3)
# KF, RTS
M11x, mu11x = fil.smoothing_filter(arr_11x)
M11y, mu11y = fil.smoothing_filter(arr_11y)
M11z, mu11z = fil.smoothing_filter(arr_11z)

# Left knee
arr_12x = joint_12['joint_x'].to_numpy()
arr_12y = joint_12['joint_y'].to_numpy()
arr_12z = joint_12['joint_z'].to_numpy()

# BW
z12x, z2_12x, y12x = f.digital_filter(arr_12x, 3)
z12y, z2_12y, y12y = f.digital_filter(arr_12y, 3)
z12z, z2_12z, y12z = f.digital_filter(arr_12z, 3)
# KF, RTS
M12x, mu12x = fil.smoothing_filter(arr_12x)
M12y, mu12y = fil.smoothing_filter(arr_12y)
M12z, mu12z = fil.smoothing_filter(arr_12z)

# Left ankle
arr_13x = joint_13['joint_x'].to_numpy()
arr_13y = joint_13['joint_y'].to_numpy()
arr_13z = joint_13['joint_z'].to_numpy()

# BW
z13x, z2_13x, y13x = f.digital_filter(arr_13x, 3)
z13y, z2_13y, y13y = f.digital_filter(arr_13y, 3)
z13z, z2_13z, y13z = f.digital_filter(arr_13z, 3)
# KF, RTS
M13x, mu13x = fil.smoothing_filter(arr_13x)
M13y, mu13y = fil.smoothing_filter(arr_13y)
M13z, mu13z = fil.smoothing_filter(arr_13z)

# Create list with x,y,z coords together (unfiltered coordinates)
uarr8, uarr9, uarr10, uarr11, uarr12, uarr13 = ([] for i in range(6))

for i in range(0, len(y8x) - 1):
    ua8 = [arr_8x[i], arr_8y[i], arr_8z[i]]
    uarr8.append(ua8)

for i in range(0, len(y9x) - 1):   
    ua9 = [arr_9x[i], arr_9y[i], arr_9z[i]]
    uarr9.append(ua9)

for i in range(0, len(y10x) - 1):
    ua10 = [arr_10x[i], arr_10y[i], arr_10z[i]]
    uarr10.append(ua10)

for i in range(0, len(y11x) - 1):
    ua11 = [arr_11x[i], arr_11y[i], arr_11z[i]]
    uarr11.append(ua11)

for i in range(0, len(y12x) - 1):
    ua12 = [arr_12x[i], arr_12y[i], arr_12z[i]]
    uarr12.append(ua12)

for i in range(0, len(y13x) - 1):
    ua13 = [arr_13x[i], arr_13y[i], arr_13z[i]]
    uarr13.append(ua13)

# Create lists with x,y,z coords together (filtered BW coordinates)
arr8, arr9, arr10, arr11, arr12, arr13 = ([] for i in range(6))

for i in range(0, len(y8x) - 1):
    a8 = [y8x[i], y8y[i], y8z[i]]
    arr8.append(a8)

for i in range(0, len(y9x) - 1):   
    a9 = [y9x[i], y9y[i], y9z[i]]
    arr9.append(a9)

for i in range(0, len(y10x) - 1):
    a10 = [y10x[i], y10y[i], y10z[i]]
    arr10.append(a10)

for i in range(0, len(y11x) - 1):
    a11 = [y11x[i], y11y[i], y11z[i]]
    arr11.append(a11)

for i in range(0, len(y12x) - 1):
    a12 = [y12x[i], y12y[i], y12z[i]]
    arr12.append(a12)

for i in range(0, len(y13x) - 1):
    a13 = [y13x[i], y13y[i], y13z[i]]
    arr13.append(a13)

# Create lists with x,y,z coords together (filtered KF, RTS coordinates)
karr8, karr9, karr10, karr11, karr12, karr13 = ([] for i in range(6))
rarr8, rarr9, rarr10, rarr11, rarr12, rarr13 = ([] for i in range(6))

for i in range(0, len(mu8x) - 1):
    ka8 = [mu8x[i][0], mu8y[i][0], mu8z[i][0]]
    karr8.append(ka8)
    ra8 = [M8x[i][0], M8y[i][0], M8z[i][0]]
    rarr8.append(ra8)

for i in range(0, len(mu9x) - 1):
    ka9 = [mu9x[i][0], mu9y[i][0], mu9z[i][0]]
    karr9.append(ka9)
    ra9 = [M9x[i][0], M9y[i][0], M9z[i][0]]
    rarr9.append(ra9)

for i in range(0, len(mu10x) - 1):
    ka10 = [mu10x[i][0], mu10y[i][0], mu10z[i][0]]
    karr10.append(ka10)
    ra10 = [M10x[i][0], M10y[i][0], M10z[i][0]]
    rarr10.append(ra10)

for i in range(0, len(mu11x) - 1):
    ka11 = [mu11x[i][0], mu11y[i][0], mu11z[i][0]]
    karr11.append(ka11)
    ra11 = [M11x[i][0], M11y[i][0], M11z[i][0]]
    rarr11.append(ra11)

for i in range(0, len(mu12x) - 1):
    ka12 = [mu12x[i][0], mu12y[i][0], mu12z[i][0]]
    karr12.append(ka12)
    ra12 = [M12x[i][0], M12y[i][0], M12z[i][0]]
    rarr12.append(ra12)

for i in range(0, len(mu13x) - 1):
    ka13 = [mu13x[i][0], mu13y[i][0], mu13z[i][0]]
    karr13.append(ka13)
    ra13 = [M13x[i][0], M13y[i][0], M13z[i][0]]
    rarr13.append(ra13)

#--------END FILTERING--------#

#--------START FIX SIZE--------#

# Get the same length (unfiltered coordinates)
ur8, ur9, ur10 = get_same_length(uarr8, uarr9, uarr10)
ur11, ur12, ur13 = get_same_length(uarr11, uarr12, uarr13)

# Get the same length (filtered BW coordinates) 
r8, r9, r10 = get_same_length(arr8, arr9, arr10)
r11, r12, r13 = get_same_length(arr11, arr12, arr13)

# Get the same length (filtered KF, RTS coordinates) 
kr8, kr9, kr10 = get_same_length(karr8, karr9, karr10)
kr11, kr12, kr13 = get_same_length(karr11, karr12, karr13)
rr8, rr9, rr10 = get_same_length(rarr8, rarr9, rarr10)
rr11, rr12, rr13 = get_same_length(rarr11, rarr12, rarr13)

#--------END FIX SIZE--------#

#--------START 3D ANGLE CALCULATIONS--------#

# Calculate theta angle for right knee (unfiltered coordinates)
un_theta_right, un_theta_left = ([] for i in range(2))
for i in range(0, len(ur8) - 1):
    un_th_right = a.calculate_3d_angle(np.asarray(ur8[i]), np.asarray(ur9[i]), np.asarray(ur10[i]))
    un_theta_right.append(un_th_right)

# Calculate theta angle for left knee (unfiltered coordinates)
for i in range(0, len(ur11) - 1):
    un_th_left = a.calculate_3d_angle(np.asarray(ur11[i]), np.asarray(ur12[i]), np.asarray(ur13[i]))
    un_theta_left.append(un_th_left)

# Calculate theta angle for right knee (filtered BW coordinates)
theta_right, theta_left = ([] for i in range(2))
for i in range(0, len(r8) - 1):
    th_right = a.calculate_3d_angle(np.asarray(r8[i]), np.asarray(r9[i]), np.asarray(r10[i]))
    theta_right.append(th_right)

# Calculate theta angle for left knee (filtered BW coordinates)
for i in range(0, len(r11) - 1):
    th_left = a.calculate_3d_angle(np.asarray(r11[i]), np.asarray(r12[i]), np.asarray(r13[i]))
    theta_left.append(th_left)

# Calculate theta angle for right knee (filtered KF, RTS coordinates)
kf_theta_right, kf_theta_left, rts_theta_right, rts_theta_left= ([] for i in range(4))
for i in range(0, len(kr8) - 1):
    kf_th_right = a.calculate_3d_angle(np.asarray(kr8[i]), np.asarray(kr9[i]), np.asarray(kr10[i]))
    kf_theta_right.append(kf_th_right)
    rts_th_right = a.calculate_3d_angle(np.asarray(rr8[i]), np.asarray(rr9[i]), np.asarray(rr10[i]))
    rts_theta_right.append(rts_th_right)

# Calculate theta angle for left knee (filtered KF, RTS coordinates)
for i in range(0, len(kr11) - 1):
    kf_th_left = a.calculate_3d_angle(np.asarray(kr11[i]), np.asarray(kr12[i]), np.asarray(kr13[i]))
    kf_theta_left.append(kf_th_left)
    rts_th_left = a.calculate_3d_angle(np.asarray(rr11[i]), np.asarray(rr12[i]), np.asarray(rr13[i]))
    rts_theta_left.append(rts_th_left)

#--------END 3D ANGLE CALCULATIONS--------#

#--------START STATISTICS--------#

# Calculate std_dev and variance for unfiltered and filtered coordinates

stats_log_theta_right, per_theta_right = stats.stats_log(theta_right)
stats_log_theta_left, per_theta_left = stats.stats_log(theta_left)
stats_log_un_theta_right, per_un_theta_right = stats.stats_log(un_theta_right)
stats_log_un_theta_left, per_un_theta_left = stats.stats_log(un_theta_left)
stats_log_theta_right_KF, per_theta_right_KF = stats.stats_log(kf_theta_right)
stats_log_theta_left_KF, per_theta_left_KF = stats.stats_log(kf_theta_left)
stats_log_theta_right_RTS, per_theta_right_RTS = stats.stats_log(rts_theta_right)
stats_log_theta_left_RTS, per_theta_left_RTS = stats.stats_log(rts_theta_left)

#--------END STATISTICS--------#

#--------START VISUALIZATION--------#

# Visualize right and left knee angle (unfiltered data)
fig, (ax1,ax2) = plt.subplots(1,2)
ax1.plot(un_theta_right)
ax1.set_title('Knee Right (unfiltered)')
ax1.set(xlabel = 'Frames', ylabel = 'Knee angle (degrees)')

ax2.plot(un_theta_left)
ax2.set_title('Knee Left (unfiltered)')
ax2.set(xlabel = 'Frames', ylabel = 'Knee angle (degrees)')

plt.show()

# Visualize log stats for knee angle (unfiltered data)
stats.visualization(stats_log_un_theta_right, stats_log_un_theta_left, 'Knee right Unfiltered', 'Knee left Unfiltered')

# Visualize right and left knee angle (filtered data)
fig, (ax3,ax4) = plt.subplots(1,2)
ax3.plot(theta_right)
ax3.set_title('Knee Right BW')
ax3.set(xlabel = 'Frames', ylabel = 'Knee angle (degrees)')

ax4.plot(theta_left)
ax4.set_title('Knee Left BW')
ax4.set(xlabel = 'Frames', ylabel = 'Knee angle (degrees)')

plt.show()

# Visualize log stats for knee angle (filtered  BW data)
stats.visualization(stats_log_theta_right, stats_log_theta_left, 'Knee right BW', 'Knee left BW')

# Visualization of RTS 
fil.double_visualization(kf_theta_right, rts_theta_right, kf_theta_left, rts_theta_left,
                        'Knee Right', 'Knee Left')

# Visualisation stats log of KF and RTS
stats.visualization(stats_log_theta_left_KF, stats_log_theta_right_KF, 'Left knee KF', 'Right knee KF')
#stats.visualization(stats_log_theta_right_RTS, stats_log_theta_left_RTS, 'Knee right RTS', 'Knee left RTS')
#stats.visualization(stats_log_theta_right_KF, stats_log_theta_right_RTS, 'Knee right KF', 'Knee right RTS')
#stats.visualization(stats_log_un_theta_right, stats_log_theta_right_KF, 'Knee right (unfiltered)', 'Knee right (KL)')

# Plot all together (from unfiltered to filtered angles)
fig, (ax1, ax2) = plt.subplots(1,2)
ax1.plot(un_theta_right, c = 'black', label = 'Unfiltered', alpha = 0.5)
ax1.plot(theta_right, c = 'cyan', label = 'BW')
ax1.plot(kf_theta_right, c = 'yellow', label = 'KF')
ax1.plot(rts_theta_right, c = 'r', label = 'RTS')
ax1.set(xlabel = 'Frames', ylabel = 'Knee angle (degrees)')
ax1.set_title('Knee Right')
ax1.set_facecolor('grey')

ax2.plot(un_theta_left, c = 'black', label = 'Unfiltered', alpha = 0.5)
ax2.plot(theta_left, c = 'cyan', label = 'BW')
ax2.plot(kf_theta_left, c = 'yellow', label = 'KF')
ax2.plot(rts_theta_left, c = 'r', label = 'RTS')
ax2.set(xlabel = 'Frames')
ax2.set_title('Knee Left')
ax2.set_facecolor('grey')

plt.legend(loc = 4)
plt.show()

#--------END VISUALIZATION--------#

#--------START PERCENTILES--------#

# Print percentiles as DataFrames
""" per_list = [per_un_theta_right, per_un_theta_left, per_theta_right, per_theta_left, per_theta_right_KF, per_theta_left_KF,
            per_theta_right_RTS, per_theta_left_RTS]
per_names = ['Knee Right Unfiltered:', 'Knee Left Unfiltered:', 'Knee Right BW:', 'Knee Left BW:', 
            'Knee Right KF:', 'Knee Left KF:', 'Knee Right RTS:', 'Knee Left RTS:']

for i in range(0, len(per_list)):
    df = pd.DataFrame(per_list[i], columns = [per_names[i]])
    df = df.T
    df.rename(columns = {0: '5th', 1: '25th', 2: '50th', 3: '75th', 4: '90th', 5: '99th'}, inplace = True)
    print(df) """

#--------END PERCENTILES--------#


######
##
### Delete it after FOI presentation
##
######
ground_truth_right = [180] * len(rts_theta_right)
ground_truth_left = [180] * len(rts_theta_left)

mse_right = mean_squared_error(ground_truth_right, rts_theta_right)
mse_left = mean_squared_error(ground_truth_left, rts_theta_left)

mae_right = mean_absolute_error(ground_truth_right, rts_theta_right)
mae_left = mean_absolute_error(ground_truth_left, rts_theta_left)

mae_right = int(mae_right*100)/100
mae_left = int(mae_left*100)/100


font = {'family': 'serif',
        'color':  'black',
        'weight': 'bold',
        'size': 12,
        }

plt.plot(ground_truth_right, c = 'black', alpha = 0.5, label = 'Theoritical GT', linewidth = 2.5)
plt.plot(rts_theta_right, c = 'darkcyan', label = 'Right knee', linewidth = 2)
plt.plot(rts_theta_left, c = 'darkred', label = 'Left knee', linewidth = 2)
plt.title('Standstill subject/Non-static camera', weight = 'bold', pad = 15)
plt.ylabel('Degrees', fontsize = 14, fontweight = 'bold')
plt.xlabel('Frames', fontsize = 14, fontweight = 'bold')
plt.text(1100, 147, 'MAE right:' + str(mae_right), fontdict = font)
plt.text(1100, 144, 'MAE left:' + str(mae_left), fontdict = font)

ax = plt.gca()
ax.set_axisbelow(True)
ax.yaxis.grid(True, color='#EEEEEE')
ax.xaxis.grid(False)

plt.legend()
plt.show()

# Bar chart plots of stats logging
fig, (ax0, ax1) = plt.subplots(1,2)
bars0 = ax0.bar(*zip(*stats_log_theta_left_KF.items()), color = 'darkcyan')
ax0.spines['top'].set_visible(False)
ax0.spines['right'].set_visible(False)
ax0.spines['left'].set_visible(False)
ax0.spines['bottom'].set_color('#DDDDDD')
ax0.set_title('Left knee after KF', weight = 'bold', pad = 15, c = 'peru')
ax0.set_ylabel('[min,mean,median,max,mode,std_dev] = deg, [variance] = deg^2', fontsize = 12, fontweight = 'bold', color = 'peru')
ax0.set_axisbelow(True)
ax0.yaxis.grid(True, color='#EEEEEE')
ax0.xaxis.grid(False)

bar_color_0 = bars0[0].get_facecolor()
for bar in bars0:
    ax0.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 1,
        round(bar.get_height(), 2),
        horizontalalignment = 'center',
        color = bar_color_0,
        weight='bold'
    )

bars1 = ax1.bar(*zip(*stats_log_theta_right_KF.items()), color = 'darkcyan')
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.spines['left'].set_visible(False)
ax1.spines['bottom'].set_color('#DDDDDD')
ax1.set_title('Right knee after KF', weight = 'bold', pad = 15, c = 'peru')
ax1.set_axisbelow(True)
ax1.yaxis.grid(True, color='#EEEEEE')
ax1.xaxis.grid(False)

bar_color_1 = bars1[0].get_facecolor()
for bar in bars1:
    ax1.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 1,
        round(bar.get_height(), 2),
        horizontalalignment = 'center',
        color = bar_color_1,
        weight='bold'
    )

plt.show()


# Animation
""" a = Animations(rts_theta_left, 'animation')
a.anime_plot(30)
a.save_as_gif()
a.gif_to_mp4()
q = Animations(rts_theta_right, 'animation_r')
q.anime_plot(30)
q.save_as_gif()
q.gif_to_mp4() """