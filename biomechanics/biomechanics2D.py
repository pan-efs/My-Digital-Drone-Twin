import math
import numpy as np
import pandas as pd

from exceptions.movement_analysis import ShapeDataFrame2DError, ColNamesDataFrame2DError

def __errors__(data: pd.DataFrame):
    """
    A helper function in order to catch errors relevant to DataFrame features.
    
    :type data: pd.DataFrame
    
    :raises ShapeDataFrame2DError: See exceptions.movement_analysis.py
    :raises ColNamesDataFrame2DError: See exceptions.movement_analysis.py
    """
    if data.shape[1] != 3:
            raise ShapeDataFrame2DError
        
    cols = data.columns
    if cols[0] != 'time' or cols[1] != 'joint_x' or cols[2] != 'joint_y':
        raise ColNamesDataFrame2DError


class AngularKinematics:
    def __init__(self):
        pass
    
    def normalize_2d_coordinates(self, arr, img_height, img_width):
        """
        Helper function which normalizes 2D coordinates.
        
        :param arr: (x, y) coordinates
        :type arr: array
        :param img_height: height dimension
        :type img_height: int
        :param img_width: width dimension
        :type img_width: int
        
        :return: normalized array with 2D coordinates
        :rtype: array
        """
        for i in range(0, len(arr)):
            arr[i][0] = arr[i][0]/img_height
            arr[i][1] = arr[i][1]/img_width
        
        return arr
    
    def calculate_abs_angle(self, proximal, distal):
        """
        Calculates the absolute angle of a body segment on 2D saggital plane relative to right horizontal.
        
        :param proximal: proximal's position
        :type proximal: pd.DataFrame
        :param distal: distal's position
        :type distal: pd.DataFrame
        
        :return: angle in degrees
        :rtype: float
        """
        y = proximal[1] - distal[1]
        x = proximal[0] - distal[0]
        div = y / x

        if y > 0 and x > 0:
            theta = math.degrees(math.atan(div))
        elif y > 0 and x < 0:
            theta = math.degrees(math.atan(div)) + 180
        elif y < 0 and x < 0:
            theta = math.degrees(math.atan(div)) + 180
        else:
            theta = math.degrees(math.atan(div)) + 360

        return theta
    
    def calculate_rel_angle(self, proximal: pd.DataFrame, centre: pd.DataFrame, distal: pd.DataFrame):
        """
        Calculates the relative angle between longitudinal axes of two segments.
        It is also reffered to joint angle or intersegmental angle.
        
        :param proximal: proximal's position
        :type proximal: pd.DataFrame
        :param centre: centre's position
        :type centre: pd.DataFrame
        :param distal: distal's position
        :type distal: pd.DataFrame
        
        :return: angle in degrees
        :rtype: float
        """
        a = math.sqrt(
            math.pow((proximal[0] - distal[0]), 2)
            + math.pow((proximal[1] - distal[1]), 2)
        )
        b = math.sqrt(
            math.pow((proximal[0] - centre[0]), 2)
            + math.pow((proximal[1] - centre[1]), 2)
        )
        c = math.sqrt(
            math.pow((centre[0] - distal[0]), 2) + math.pow((centre[1] - distal[1]), 2)
        )

        theta = math.degrees(
            math.acos(
                (-((math.pow(a, 2) - math.pow(b, 2) - math.pow(c, 2)) / (2 * b * c)))
            )
        )

        return theta
    
    def calculate_relative_angle(self, proximal: np.array, centre: np.array, distal: np.array):
        """
        Calculates the relative angle between longitudinal axes of two segments.
        It is also reffered to joint angle or intersegmental angle.
        
        :param proximal: proximal's position
        :type proximal: np.array
        :param centre: centre's position
        :type centre: np.array
        :param distal: distal's position
        :type distal: np.array
        
        :return: angle in degrees
        :rtype: list
        """
        length = proximal.shape[0]
        theta = []
        
        for i in range(0, length-1):
            a = math.sqrt(
            math.pow((proximal[i][0] - distal[i][0]), 2)
            + math.pow((proximal[i][1] - distal[i][1]), 2)
            )
            
            b = math.sqrt(
            math.pow((proximal[i][0] - centre[i][0]), 2)
            + math.pow((proximal[i][1] - centre[i][1]), 2)
            )
            
            c = math.sqrt(
            math.pow((centre[i][0] - distal[i][0]), 2) 
            + math.pow((centre[i][1] - distal[i][1]), 2)
            )
            
            try:
                th = math.degrees(
                math.acos(
                (-((math.pow(a, 2) - math.pow(b, 2) - math.pow(c, 2)) / (2*b*c)))
                ))
                theta.append(th)
            except ValueError:
                th = theta[i - 1]
                theta.append(th)
        
        return theta
    
    def calculate_hip_angle(self, abs_thigh, abs_trunk):
        """
        Calculates the hip angle using absolute angles.
        The right side of the subject's body is closest to the camera and is considered to be in the x-y plane.
        
        :param abs_leg: absolute angle of thigh
        :type abs_leg: array
        :param abs_foot: absolute angle of trunk
        :type abs_foot: array
        
        :return: angle in degrees
        :rtype: float
        """
        theta = abs_thigh - abs_trunk
        return theta
    
    def calculate_knee_angle(self, abs_thigh, abs_leg):
        """
        Calculates the knee angle using absolute angles.
        The right side of the subject's body is closest to the camera and is considered to be in the x-y plane.
        
        :param abs_leg: absolute angle of thigh
        :type abs_leg: array
        :param abs_foot: absolute angle of leg
        :type abs_foot: array
        
        :return: angle in degrees
        :rtype: float
        """
        theta = abs_thigh - abs_leg
        return theta
    
    def calculate_ankle_angle(self, abs_leg, abs_foot):
        """
        Calculates the ankle angle using absolute angles.
        The right side of the subject's body is closest to the camera and is considered to be in the x-y plane.
        
        :param abs_leg: absolute angle of leg
        :type abs_leg: array
        :param abs_foot: absolute angle of foot
        :type abs_foot: array
        
        :return: angle in degrees
        :rtype: float
        """
        theta = abs_leg - abs_foot + 90
        return theta


class LinearKinematics:
    def __init__(self):
        pass
    
    def calculate_velocity(self, data: pd.DataFrame):
        """
        Calculates velocity for horizontal and vertical components using the first central difference method.
        Velocity is calculated between two video frames.
        Pre-requisite: analyze a video offline knowing in before fps.
        
        :param data: a dataframe including time interval, horizontal position and vertical position.
        :type data: pd.DataFrame
        
        :return: new time, horizontal velocity and vertical velocity
        :rtype: list
        """
        __errors__(data)
        
        time = []
        vel_x = []
        vel_y = []

        for i in range(1, len(data) - 1):
            x = (data.at[i + 1, "joint_x"] - data.at[i - 1, "joint_x"]) / (
                data.at[i + 1, "time"] - data.at[i - 1, "time"]
            )
            y = (data.at[i + 1, "joint_y"] - data.at[i - 1, "joint_y"]) / (
                data.at[i + 1, "time"] - data.at[i - 1, "time"]
            )
            time.append(data.at[i, "time"])
            vel_x.append(x)
            vel_y.append(y)

        return time, vel_x, vel_y
    
    def cal_velocity(self, time, data):
        """
        Calculates velocity for horizontal and vertical components using the first central difference method.
        Velocity is calculated between two video frames.
        Pre-requisite: analyze a video offline knowing in before fps.
        
        :param time: time interval
        :type time: array
        :param data: desired joint velocity data
        :type data: array
        
        :return: new time, horizontal velocity and vertical velocity
        :rtype: list
        """
        new_time = []
        vel_x = []
        vel_y = []

        for i in range(1, len(data) - 1):
            x = (data[i + 1][0] - data[i - 1][0]) / (
                time[i + 1] - time[i - 1]
            )
            y = (data[i + 1][1] - data[i - 1][1]) / (
                time[i + 1] - time[i - 1]
            )
            new_time.append(time[i])
            vel_x.append(x)
            vel_y.append(y)

        return new_time, vel_x, vel_y
    
    def calculate_acceleration(self, data: pd.DataFrame):
        """
        Calculates acceleration for horizontal and vertical components using the first central difference method.
        Acceleration is calculated between two video frames.
        Pre-requisite: analyze a video offline knowing in before fps.
        
        :param data: a dataframe including time interval, horizontal velocity and vertical velocity.
        :type data: pd.DataFrame
        
        :return: new time, horizontal velocity and vertical velocity
        :rtype: list
        """
        __errors__(data)
        
        time = []
        acc_x = []
        acc_y = []

        for i in range(1, len(data) - 1):
            x = (data.at[i + 1, "velocity_x"] - data.at[i - 1, "velocity_x"]) / (
                data.at[i + 1, "time"] - data.at[i - 1, "time"]
            )
            y = (data.at[i + 1, "velocity_y"] - data.at[i - 1, "velocity_y"]) / (
                data.at[i + 1, "time"] - data.at[i - 1, "time"]
            )
            time.append(data.at[i, "time"])
            acc_x.append(x)
            acc_y.append(y)
            
        return time, acc_x, acc_y
    
    def cal_acceleration(self, time, data):
        """
        Calculates acceleration for horizontal and vertical components using the first central difference method.
        Acceleration is calculated between two video frames.
        Pre-requisite: analyze a video offline knowing in before fps.
        
        :param time: time interval
        :type time: array
        :param data: desired joint's velocity data
        :type data: array
        
        :return: new time, horizontal acceleration, vertical acceleration
        :rtype: list
        """
        
        new_time = []
        acc_x = []
        acc_y = []
        
        for i in range(1, len(data) - 1):
            x = (data[i + 1][0] - data[i - 1][0]) / (
                time[i + 1] - time[i - 1]
            )
            y = (data[i + 1][1] - data[i - 1][1]) / (
                time[i + 1] - time[i - 1]
            )
            new_time.append(time[i])
            acc_x.append(x)
            acc_y.append(y)
        
        return new_time, acc_x, acc_y
    
    def calculate_speed(self, data):
        """
        Calculates speed from 2D coordinates (x, y) using the first central difference method.
        Speed is calculated between two video frames.
        
        :param data: a dataframe including time interval, joint x position and joint y position.
        :type data: pd.DataFrame
        
        :return: new time, speed
        :rtype: list
        """
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
            vel = math.sqrt(math.pow(x, 2) + math.pow(y, 2))
            time.append(data.at[i, "time"])
            speed.append(vel)

        return time, speed
    
    def cal_speed(self, time, data):
        """
        Calculates speed from 2D coordinates (x, y) using the first central difference method.
        Speed is calculated between two video frames.
        
        :param time: time interval
        :type time: array
        :param data: desired joint's position data
        :type data: array
        
        :return: new time, speed
        :rtype: list
        """
        new_time = []
        speed = []
        
        for i in range(1, len(data) - 1):
            x = (data[i + 1][0] - data[i - 1][0]) / (
                time[i + 1] - time[i - 1]
            )
            y = (data[i + 1][1] - data[i - 1][1]) / (
                time[i + 1] - time[i - 1]
            )
            s = math.sqrt(x*x + y*y)
            speed.append(s)
            new_time.append(time[i])
        
        return new_time, speed
    
    def calculate_displacement(self, data: pd.DataFrame):
        """
        Calculate the horizontal and vertical displacement using 2D coordinates, as well as the resultant displacement.
        First central defference method.
        
        :param data: a dataframe including time interval, joint x position and joint y position.
        :type data: pd.DataFrame
        
        :return: new time, dx, dy, resultant
        :rtype: list
        """
        __errors__(data)
        
        time = []
        dx = []
        dy = []
        r = []
        
        for i in range(0, len(data) - 1):
            deltaX = (data.at[i + 1, 'joint_x'] - data.at[i, 'joint_x'])
            
            deltaY = (data.at[i + 1, 'joint_y'] - data.at[i, 'joint_y'])
            
            resultant = math.sqrt(deltaX*deltaX + deltaY*deltaY)
            
            time.append(data.at[i, "time"])
            dx.append(deltaX)
            dy.append(deltaY)
            r.append(resultant)
        
        return time, dx, dy, r
    
    def cal_displacement(self, time, data):
        """
        Calculate the horizontal and vertical displacement using 2D coordinates, as well as the resultant displacement.
        First central defference method.
        
        :param time: time interval
        :type time: array
        :param data: desired joints position data
        :type data: array
        
        :return: new time, dx, dy, resultant
        :rtype: list
        """
        
        new_time = []
        dx = []
        dy = []
        r = []
        
        for i in range(0, len(data) - 1):
            deltaX = data[i + 1][0] - data[i][0]
            
            deltaY = data[i + 1][1] - data[i][1]
            
            resultant = math.sqrt(deltaX*deltaX + deltaY*deltaY)
            
            new_time.append(time[i])
            dx.append(deltaX)
            dy.append(deltaY)
            r.append(resultant)
            
        return new_time, dx, dy, r

class Energy:
    def __init__(self):
        pass
    
    def energy_expenditure(self, speed):
        """
        Estimates the energy expenditure based to velocity.
        Equation derives from 'Energy-speed relation and optimal speed during level walking (1958)' article.
        
        :param speed: speed in m/min
        :type speed: float
        
        :return: energy expenditure in cal/m/kg
        :rtype: float
        """
        e = 29 / speed + 0.0053 * speed
        return e