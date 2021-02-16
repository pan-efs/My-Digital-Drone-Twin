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
        
        time = []
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
            time.append(data.at[i, "time"])
            
        return time, speed
    
    
    """
    Description: [text]:
    Calculate the horizontal and vertical displacement using 3D coordinates, as well as the resultant displacement.
    First central defference method.
    
    Parameters: [dataframe]: [time, joint_x, joint_y, joint_z]
    
    Returns: [tuple]: time, dx, dy, dz, r
    """
    def calculate_displacement(self, data):
        
        if data.shape[1] != 4:
            print('Dataframe should have four columns.')
            return 1
        
        time = []
        r = []
        dx = []
        dy = []
        dz = []
        
                
        for i in range(0, len(data) - 1):
            deltaX = (data.at[i + 1, 'joint_x'] - data.at[i, 'joint_x'])
            
            deltaY = (data.at[i + 1, 'joint_y'] - data.at[i, 'joint_y'])
            
            deltaZ = (data.at[i + 1, 'joint_z'] - data.at[i, 'joint_z'])
            
            resultant = math.sqrt(deltaX*deltaX + deltaY*deltaY + deltaZ*deltaZ)
            
            time.append(data.at[i, "time"])
            dx.append(deltaX)
            dy.append(deltaY)
            dz.append(deltaZ)
            r.append(resultant)
            
        return time, dx, dy, dz, r
        