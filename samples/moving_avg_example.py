import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from filters.moving_average import MovingAverage as MovingAverage

file_path = 'C:\\Users\\Drone\\Desktop\\Panagiotis\\My-Digital-Drone-Twin\\cubemos\\lower_body_example.txt'

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

# Example with left knee
kneeLeftX = []
kneeLeftY = []
for i in range(0, len(knee_left_array)):
    kneeLeftX.append(knee_left_array[i][0])
    kneeLeftY.append(knee_left_array[i][1])

p = MovingAverage()
mX = p.moving_average(kneeLeftX, 3)
mY = p.moving_average(kneeLeftY, 3)

plt.plot(kneeLeftX)
plt.plot(mX)
plt.show()

plt.plot(kneeLeftY)
plt.plot(mY)
plt.show()