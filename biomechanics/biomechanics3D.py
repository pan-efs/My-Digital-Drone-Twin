import pandas as pd
import numpy as np
import math

class LinearKinematics:
    """
    Description: [text]:
    Calculates speed from x,y,z axis values using the first central difference method.
    Speed is calculated between two video frames.
    Pre-requisite: analyze a video offline knowing in before fps.
    
    """

    "Parameters: [dataframe]: [time, joint_x, joint_y, joint_z]"

    "Returns: [tuple]: [speed],  [units]: m/s"

    def calculate_speed(self, data):

        if data.shape[1] != 4:
            print("DataFrame should have four columns.")
            return 1

        speed = []

        for i in range(1, len(data) - 1):
            x = (data.at[i + 1, "joint_x"] - data.at[i - 1, "joint_x"]) / (
                data.at[i + 1, "time"] - data.at[i - 1, "time"]
            )
            y = (data.at[i + 1, "joint_y"] - data.at[i - 1, "joint_y"]) / (
                data.at[i + 1, "time"] - data.at[i - 1, "time"]
            )
            z = (data.at[i + 1, "joint_z"] - data.at[i - 1, "joint_z"]) / (
                data.at[i + 1, "time"] - data.at[i - 1, "time"]
            )
            vel = math.sqrt(math.pow(x, 2) + math.pow(y, 2) + math.pow(z, 2))
            speed.append(vel)
            
        return speed
    
k = LinearKinematics()
data = [[0.0000, 0.00, 0.00, 0.00], [0.0167, 0.10, 0.15, 0.20], [0.0334, 0.12, 0.22, 0.28], [0.0501, 0.15, 0.27, 0.35]]
df = pd.DataFrame(data = data, columns=['time', 'joint_x', 'joint_y', 'joint_z'])
speed = k.calculate_speed(df)
print(speed)