import pandas as pd
import numpy as np
import math
from scipy.signal import *
from matplotlib import pyplot as plt
from exceptions.movement_analysis import ShapeDataFrame3DError, ColNamesDataFrame3DError, FpsError

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
    
class Magnitude:
    def __init__(self, data: list):
        self.data = data
        self.mag_ls = []
        self.maximum = 0
        self.minimum = 0
    
    def calculate_magnitude(self):
        """
        Calculate the 3D magnitude of each list in a list.

        :type data: lists of list
        
        :return: Magnitude for each x-y-z pair.
        :rtype: list
        """
        
        for i in range(0, len(self.data)):
            mag = self.data[i][0]*self.data[i][0] + self.data[i][1]*self.data[i][1] + self.data[i][2]*self.data[i][2]
            self.mag_ls.append(mag)
    
        return self.mag_ls
    
    def find_visualize_local_max_min(self, name: str = 'Title', show: bool = False):
        """
        Visualizes local maximums and minimums of a line plot.
        Useful in order to estimate the cadence of repetitive movements, such as cycling.

        :type fil_ls: list, array (filtered is recommended)
        :type name: name of the plot
        :type show: If True, then it plots. Otherwise, no.
        
        """
        df = pd.DataFrame(self.mag_ls, columns = ['fil_ls'])
        df['min'] = df.iloc[argrelextrema(df.fil_ls.values, np.less_equal,
                    order=3)[0]]['fil_ls']
        df['max'] = df.iloc[argrelextrema(df.fil_ls.values, np.greater_equal,
                    order=3)[0]]['fil_ls']
        
        self.maximum = len(df['max']) - df['max'].isnull().sum()
        self.minimum = len(df['min']) - df['min'].isnull().sum()
        
        fig, ax = plt.subplots()
        ax.scatter(df.index, df['min'], c='r', label = str(self.minimum))
        ax.scatter(df.index, df['max'], c='g', label = str(self.maximum))
        plt.title(name)
        plt.xlabel('Frames')
        plt.ylabel('Magnitude')
        ax.plot(df.index, df['fil_ls'])
        
        if show == True:
            plt.show()
        
        return self.maximum, self.minimum
    
class Cadence:
    
    def __init__(self, magnitude_data):
        self.threshold = [1800, 2400, 7200, 10800, 14400, 18000]
        self.magnitude = magnitude_data
        self.length_data_per_min = 0 # according to fps
        
    def calculate_cadence(self, maximum, fps: int = 30):
        
        if fps == 30:
            self.length_data_per_min = self.threshold[0]
        elif fps == 60:
            self.length_data_per_min = self.threshold[1]
        elif fps == 120:
            self.length_data_per_min = self.threshold[2]
        elif fps == 180:
            self.length_data_per_min = self.threshold[3]
        elif fps == 240:
            self.length_data_per_min = self.threshold[4]
        elif fps == 300:
            self.length_data_per_min = self.threshold[5]
        else:
            raise FpsError
        
        duration = int(len(self.magnitude)/fps)
        
        cadence = maximum * (60 / (duration))
        
        return int(np.ceil(cadence)), duration
