import pandas as pd
import numpy as np
import math
from exceptions.movement_analysis import ShapeDataFrame3DError, ColNamesDataFrame3DError

def __errors__(data: pd.DataFrame):
    """
    A helper function in order to catch errors relevant to DataFrame features.
    
    :type data: pd.DataFrame
    
    :raises ShapeDataFrame2DError: See exceptions.movement_analysis.py
    :raises ColNamesDataFrame2DError: See exceptions.movement_analysis.py
    """
    if data.shape[1] != 3:
            raise ShapeDataFrame3DError
        
    cols = data.columns
    if cols[0] != 'time' or cols[1] != 'joint_x' or cols[2] != 'joint_y' or cols[3] != 'joint_z':
        raise ColNamesDataFrame3DError


class AngularKinematics:
    """
    Description: [text]:
    Calculates joint angle using three 3D vectors.
    Before calling this function vectorize should be applied. For example,
    vec = np.vectorize(k.calculate_3d_angle)
    """

    "Parameters: [vectors]: [joint_x, joint_y, joint_z]"

    "Returns: [float]: [angle],  [units]: degrees"
    def calculate_3d_angle(self, A: np.ndarray, B: np.ndarray, C: np.ndarray):
        ba = A - B
        bc = C - B

        cosine = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
        angle = np.arccos(cosine)
        theta = np.degrees(angle)
        return theta
        
    
        
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
        __errors__(data)
        
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
        __errors__(data)
        
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