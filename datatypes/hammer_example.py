import numpy as np
from matplotlib import pyplot as plt

from joints_dataframe import JointsDataframe
from joints_numpys import JointsNumpys
from joints_list import JointsList
from filters.digital_filter import DigitalFilter
from filters.kalmanFilter import KalmanFilters as KalmanFilters
from filters.moving_average import MovingAverage as MovingAverage
from biomechanics.biomechanics3D import Slope
from stats.utils_stats import StatsUtils

# Data pre-processing
# We can use the desired format calling the respective class. I have commented the jDF and jNps as examples.
# clean_3d.txt works like dummy file in order to clean a text file from unnecessary characters.
# That means that clean_3d.txt file is overwritten. To avoid overwriting, you can define a distinct path.
""" jDF = JointsDataframe('C:\\Users\\Drone\\Desktop\\Panagiotis\\My-Digital-Drone-Twin\\samples\\data\\teen_male_hammer_long.txt',
                    'C:\\Users\\Drone\\Desktop\\Panagiotis\\My-Digital-Drone-Twin\\datatypes\\logging\\clean_3d.txt').__return__()

jNps = JointsNumpys('C:\\Users\\Drone\\Desktop\\Panagiotis\\My-Digital-Drone-Twin\\samples\\data\\teen_male_hammer_long.txt',
                    'C:\\Users\\Drone\\Desktop\\Panagiotis\\My-Digital-Drone-Twin\\datatypes\\logging\\clean_3d.txt').__return__() """


# If we want the app to run totally automatically, we can get the directory directly after converter.
#jl = JointsList('C:\\Users\\Drone\\Desktop\\Panagiotis\\My-Digital-Drone-Twin\\cubemos_converter\\get_3d_joints_from_video.txt',
#                'C:\\Users\\Drone\\Desktop\\Panagiotis\\My-Digital-Drone-Twin\\datatypes\\logging\\clean_3d.txt')

jl = JointsList('C:\\Users\\Drone\\Desktop\\Panagiotis\\My-Digital-Drone-Twin\\samples\\data\\teen_male_hammer_long.txt',
                'C:\\Users\\Drone\\Desktop\\Panagiotis\\My-Digital-Drone-Twin\\datatypes\\logging\\clean_3d.txt')
jLs = jl.__return__()

# Print details
print(jl.__str__())
print(jl.__repr__())

# Get all body joints
joints = []

for i in range(0, len(jLs), 3):
    x = jl._converter_to_list(jLs[i], jLs[i+1], jLs[i+2])
    joints.append(x)

# Desired ankle joints
right_ankle = joints[10] 
left_ankle = joints[13]

# Moving average filtering
mvg = MovingAverage()

# Right lower body side
mvg_rh_x = mvg.moving_average(jLs[24],6)
mvg_rh_y = mvg.moving_average(jLs[25],6)
mvg_rh_z = mvg.moving_average(jLs[26],6)

mvg_rk_x = mvg.moving_average(jLs[27],6)
mvg_rk_y = mvg.moving_average(jLs[28],6)
mvg_rk_z = mvg.moving_average(jLs[29],6)

mvg_ra_x = mvg.moving_average(jLs[30],6)
mvg_ra_y = mvg.moving_average(jLs[31],6)
mvg_ra_z = mvg.moving_average(jLs[32],6)

# Left lower body side
mvg_lh_x = mvg.moving_average(jLs[33],6)
mvg_lh_y = mvg.moving_average(jLs[34],6)
mvg_lh_z = mvg.moving_average(jLs[35],6)

mvg_lk_x = mvg.moving_average(jLs[36],6)
mvg_lk_y = mvg.moving_average(jLs[37],6)
mvg_lk_z = mvg.moving_average(jLs[38],6)

mvg_la_x = mvg.moving_average(jLs[39],6)
mvg_la_y = mvg.moving_average(jLs[40],6)
mvg_la_z = mvg.moving_average(jLs[41],6)

# Create list for moving average filtered data
mvg_right_knee, mvg_left_knee, mvg_right_ankle, mvg_left_ankle = ([] for i in range(4))

for i in range(0, len(mvg_rk_x)):
    mvg_a9 = [mvg_rk_x[i], mvg_rk_y[i], mvg_rk_z[i]]
    mvg_right_knee.append(mvg_a9)

for i in range(0, len(mvg_lk_x)):
    mvg_a12 = [mvg_lk_x[i], mvg_lk_y[i], mvg_lk_z[i]]
    mvg_left_knee.append(mvg_a12)

for i in range(0, len(mvg_ra_x)):
    mvg_a10 = [mvg_ra_x[i], mvg_ra_y[i], mvg_ra_z[i]]
    mvg_right_ankle.append(mvg_a10)

for i in range(0, len(mvg_la_x)):
    mvg_a13 = [mvg_la_x[i], mvg_la_y[i], mvg_la_z[i]]
    mvg_left_ankle.append(mvg_a13)

# Slopes
sl = Slope()

ankle_xy, ankle_xz, ankle_yz, ankle_length, knee_xy, knee_xz, knee_yz, knee_length = ([] for i in range(8))

for i in range(0, len(mvg_right_ankle[:405])):
    xy, xz, yz, length = sl.three_dim_slopes(mvg_right_ankle[i], mvg_left_ankle[i])
    ankle_xy.append(xy)
    ankle_xz.append(xz)
    ankle_yz.append(yz)
    ankle_length.append(length)
    
    _xy, _xz, _yz, _length = sl.three_dim_slopes(mvg_right_knee[i], mvg_left_knee[i])
    knee_xy.append(_xy)
    knee_xz.append(_xz)
    knee_yz.append(_yz)
    knee_length.append(_length)

# Statistics
st = StatsUtils()
log_ankle, per_ankle = st.stats_log(ankle_length)
log_knee, per_knee = st.stats_log(knee_length)

# Visualize right and left ankle's coords (unfiltered data)
fig, (ax1,ax2) = plt.subplots(1,2)
ax1.plot(jLs[30], c = 'peru', label = 'x')
ax1.plot(jLs[31], c = 'darkcyan', label = 'y')
ax1.plot(jLs[32], c = 'b', label = 'z')
ax1.set_title('Ankle Right (unfiltered)')
ax1.set(xlabel = 'Frames', ylabel = 'coords')

ax2.plot(jLs[39], c = 'peru', label = 'x')
ax2.plot(jLs[40], c = 'darkcyan', label = 'y')
ax2.plot(jLs[41], c = 'b', label = 'z')
ax2.set_title('Ankle Left (unfiltered)')
ax2.set(xlabel = 'Frames')

plt.legend()
plt.show()

# 3D plots of ankle and knee positions
fig = plt.figure()
ax = fig.gca(projection='3d')
ax.scatter(mvg_ra_x[:405], mvg_ra_y[:405], mvg_ra_z[:405], label = 'Right ankle', alpha = 0.8)
ax.scatter(mvg_la_x[:405], mvg_la_y[:405], mvg_la_z[:405], label = 'Left ankle', alpha = 0.6)
ax.set_xlabel('X (m)', fontsize = 12, fontweight = 'bold')
ax.set_ylabel('Y (m)', fontsize = 12, fontweight = 'bold')
ax.set_zlabel('Z (m)', fontsize = 12, fontweight = 'bold')
ax.set_title('Position of left and right ankle', weight = 'bold', pad = 15)

plt.legend()
plt.show()

# Bar charts of log stats 
fig, (ax0, ax1) = plt.subplots(1,2)
bars0 = ax0.bar(*zip(*log_ankle.items()), color = 'darkcyan')
ax0.spines['top'].set_visible(False)
ax0.spines['right'].set_visible(False)
ax0.spines['left'].set_visible(False)
ax0.spines['bottom'].set_color('#DDDDDD')
ax0.set_title('Ankles distance during the turning phase', weight = 'bold', pad = 15, c = 'peru')
ax0.set_ylabel('[min,mean,median,max,mode,std_dev] = m, [variance] = m^2', fontsize = 12, fontweight = 'bold', color = 'peru')
ax0.set_axisbelow(True)
ax0.yaxis.grid(True, color='#EEEEEE')
ax0.xaxis.grid(False)

bar_color_0 = bars0[0].get_facecolor()
for bar in bars0:
    ax0.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.01,
        round(bar.get_height(), 2),
        horizontalalignment = 'center',
        color = bar_color_0,
        weight='bold'
    )

bars1 = ax1.bar(*zip(*log_knee.items()), color = 'darkcyan')
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.spines['left'].set_visible(False)
ax1.spines['bottom'].set_color('#DDDDDD')
ax1.set_title('Knees distance during the turning phase', weight = 'bold', pad = 15, c = 'peru')
ax1.set_axisbelow(True)
ax1.yaxis.grid(True, color='#EEEEEE')
ax1.xaxis.grid(False)

bar_color_1 = bars1[0].get_facecolor()
for bar in bars1:
    ax1.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.01,
        round(bar.get_height(), 2),
        horizontalalignment = 'center',
        color = bar_color_1,
        weight='bold'
    )

plt.show()