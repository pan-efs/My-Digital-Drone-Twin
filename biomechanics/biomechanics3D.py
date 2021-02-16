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

    "Returns: [list]: [speed],  [units]: m/s"

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
            vel = math.sqrt(x*x + y*y + z*z)
            speed.append(vel)
            
        return speed