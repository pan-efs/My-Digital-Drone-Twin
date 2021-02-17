import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from biomechanics.biomechanics3D import LinearKinematics as LinearKinematics
from biomechanics.biomechanics3D import AngularKinematics as AngularKinematics
from filters.digital_filter import DigitalFilter as DigitalFilter

# Define the desired paths here
file_path = 'C:\\Users\\Drone\\Desktop\\Panagiotis\\My-Digital-Drone-Twin\\samples\\data\\3d_ifocam_flex_leftleg.txt'
out_path = 'C:\\Users\\Drone\\Desktop\\Panagiotis\\My-Digital-Drone-Twin\\samples\\data\\clean_3d_joints.txt'

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

# Convert .txt to dataframe
df = pd.read_csv(out_path, delimiter = ",", header = None)

# FPS and create time array
# TODO: This method looks more like a dummy timestamp, yet it works but should be modified in the future.
dt = 1/30
time_arr = []

for i in range(0, df.shape[0]):
    time_arr.append(dt*i)

# Create time dataframe
#time_df = pd.DataFrame(time_arr, columns = ['time'])

# Concat time_df with the rest of data
#df = pd.concat([time_df, df], axis = 1)

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

# Create biomechanics3D objects
k = LinearKinematics()
a = AngularKinematics()

# Create DigitalFilter object
f = DigitalFilter()

# This technique is repeated for each joint
# Right hip
arr_8x = joint_8['joint_x'].to_numpy()
arr_8y = joint_8['joint_y'].to_numpy()
arr_8z = joint_8['joint_z'].to_numpy()

z8x, z2_8x, y8x = f.digital_filter(arr_8x, 3)
z8y, z2_8y, y8y = f.digital_filter(arr_8y, 3)
z8z, z2_8z, y8z = f.digital_filter(arr_8z, 3)

# Right knee
arr_9x = joint_9['joint_x'].to_numpy()
arr_9y = joint_9['joint_y'].to_numpy()
arr_9z = joint_9['joint_z'].to_numpy()

z9x, z2_9x, y9x = f.digital_filter(arr_9x, 3)
z9y, z2_9y, y9y = f.digital_filter(arr_9y, 3)
z9z, z2_9z, y9z = f.digital_filter(arr_9z, 3)

# Right ankle
arr_10x = joint_10['joint_x'].to_numpy()
arr_10y = joint_10['joint_y'].to_numpy()
arr_10z = joint_10['joint_z'].to_numpy()

z10x, z2_10x, y10x = f.digital_filter(arr_10x, 3)
z10y, z2_10y, y10y = f.digital_filter(arr_10y, 3)
z10z, z2_10z, y10z = f.digital_filter(arr_10z, 3)

# Left hip
arr_11x = joint_11['joint_x'].to_numpy()
arr_11y = joint_11['joint_y'].to_numpy()
arr_11z = joint_11['joint_z'].to_numpy()

z11x, z2_11x, y11x = f.digital_filter(arr_11x, 3)
z11y, z2_11y, y11y = f.digital_filter(arr_11y, 3)
z11z, z2_11z, y11z = f.digital_filter(arr_11z, 3)

# Left knee
arr_12x = joint_12['joint_x'].to_numpy()
arr_12y = joint_12['joint_y'].to_numpy()
arr_12z = joint_12['joint_z'].to_numpy()

z12x, z2_12x, y12x = f.digital_filter(arr_12x, 3)
z12y, z2_12y, y12y = f.digital_filter(arr_12y, 3)
z12z, z2_12z, y12z = f.digital_filter(arr_12z, 3)

# Left ankle
arr_13x = joint_13['joint_x'].to_numpy()
arr_13y = joint_13['joint_y'].to_numpy()
arr_13z = joint_13['joint_z'].to_numpy()

z13x, z2_13x, y13x = f.digital_filter(arr_13x, 3)
z13y, z2_13y, y13y = f.digital_filter(arr_13y, 3)
z13z, z2_13z, y13z = f.digital_filter(arr_13z, 3)

# Create lists with x,y,z coords together
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

# Get the same length
# Can be occured some light differences among arrays 
r8, r9, r10 = get_same_length(arr8, arr9, arr10)
r11, r12, r13 = get_same_length(arr11, arr12, arr13)

# Calculate theta
theta = []
for i in range(0, len(r8) - 1):
        th = a.calculate_3d_angle(np.asarray(r8[i]), np.asarray(r9[i]), np.asarray(r10[i]))
        theta.append(th)

# Visualize knee angle
plt.plot(theta, c = 'g')
plt.title('Knee angle')
plt.show()