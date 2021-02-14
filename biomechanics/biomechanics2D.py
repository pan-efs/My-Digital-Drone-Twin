import pandas as pd
import numpy as np
import math


class AngularKinematics:
    """
    Helper function which normalizes 2D coordinates.
    """
    def normalize_2d_coordinates(self, arr, img_height, img_width):
        for i in range(0, len(arr)):
            arr[i][0] = arr[i][0]/img_height
            arr[i][1] = arr[i][1]/img_width
        
        return arr
        
    
    """
    Description: [text]:
    Calculates the absolute angle of a body segment on 2D saggital plane
    relative to right horizontal.
    
    """

    "Parameters: [joints]: proximal(x1,y1), distal(x2,y2)"

    "Returns: [float]: [angle in degrees]"

    def calculate_abs_angle(self, proximal, distal):
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

    """
    Description: [text]:
    Calculates the relative angle between longitudinal axes of two segments.
    It is also reffered to joint angle or intersegmental angle.
    
    """
    "Parameters: [dataframes]: proximal(x1,y1), center(x2,y2), distal(x3,y3)"

    "Returns: [float]: [angle in degrees]"
    
    # The below function is preferable
    def calculate_rel_angle(self, proximal, centre, distal):
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
    
    """
    Description: [text]:
    Calculates the relative angle between longitudinal axes of two segments.
    It is also reffered to joint angle or intersegmental angle.
    
    """
    "Parameters: [array]: proximal(x1,y1), center(x2,y2), distal(x3,y3)"

    "Returns: [array]: [float]: [angle in degrees]"
    def calculate_relative_angle(self, proximal, centre, distal):
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
                (-((math.pow(a, 2) - math.pow(b, 2) - math.pow(c, 2)) / (2 * b * c)))
                ))
                theta.append(th)
            except ValueError:
                th = theta[i - 1]
                theta.append(th)
        
        return theta

    """ 
    Description: [text]:
    Calculates the hip angle using absolute angles.
    The right side of the subject's body is closest to the camera and is considered to 
    be in the x-y plane.
    
    """
    "Parameters: [absolute angles]: absolute_angle_thigh, absolute_angle_trunk"

    "Returns: [float]: [angle in degrees]"

    def calculate_hip_angle(self, abs_thigh, abs_trunk):
        theta = abs_thigh - abs_trunk
        return theta

    """ 
    Description: [text]:
    Calculates the knee angle using absolute angles.
    The right side of the subject's body is closest to the camera and is considered to 
    be in the x-y plane.
    
    """
    "Parameters: [absolute angles]: absolute_angle_thigh, absolute_angle_leg"

    "Returns: [float]: [angle in degrees]"

    def calculate_knee_angle(self, abs_thigh, abs_leg):
        theta = abs_thigh - abs_leg
        return theta

    """ 
    Description: [text]:
    Calculates the ankle angle using absolute angles.
    The right side of the subject's body is closest to the camera and is considered to 
    be in the x-y plane.
    
    """
    "Parameters: [absolute angles]: absolute_angle_leg, absolute_angle_foot"

    "Returns: [float]: [angle in degrees]"

    def calculate_ankle_angle(self, abs_leg, abs_foot):
        theta = abs_leg - abs_foot + 90
        return theta


class LinearKinematics:

    """
    Description: [text]:
    Calculates velocity for horizontal and vertical components using the first central difference method.
    Velocity is calculated between two video frames.
    Pre-requisite: analyze a video offline knowing in before fps.
    
    """

    "Parameters: [dataframe]: [time, joint_x, joint_y]"

    "Returns: [tuple]: horizontal velocity, vertical velocity,  [units]: m/s"
    
    # The below function is preferable
    def calculate_velocity(self, data):

        if data.shape[1] != 3:
            print("DataFrame should have three columns.")
            return 1
        
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
    
    """
    Description: [text]:
    Calculates velocity for horizontal and vertical components using the first central difference method.
    Velocity is calculated between two video frames.
    Pre-requisite: analyze a video offline knowing in before fps.
    
    """

    "Parameters: [array]: [time, joint(x,y)]"

    "Returns: [tuple]: time, horizontal velocity, vertical velocity,  [units]: m/s"
    def cal_velocity(self, time, data):
        
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

    """
    Description: [text]:
    Calculates acceleration for horizontal and vertical components using the first central difference method.
    Acceleration is calculated between two video frames.
    Pre-requisite: analyze a video offline knowing in before fps.
    
    """
    "Parameters: [dataframe]: [time, velocity_x, velocity_y]"

    "Returns: [tuple]: horizontal acceleration, vertical acceleration,  [units]: m/s^2"

    # The below function is preferable
    def calculate_acceleration(self, data):

        if data.shape[1] != 3:
            print("DataFrame should have three columns.")
            return 1
        
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
    
    
    """
    Description: [text]:
    Calculates acceleration for horizontal and vertical components using the first central difference method.
    Acceleration is calculated between two video frames.
    Pre-requisite: analyze a video offline knowing in before fps.
    
    """
    "Parameters: [array]: [time, velocity]"

    "Returns: [tuple]:time, horizontal acceleration, vertical acceleration,  [units]: m/s^2"
    def cal_acceleration(self, time, data):
        
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
    
    """
    Description: [text]:
    Calculates speed from 2D coordinates (x, y) using the first central difference method.
    Speed is calculated between two video frames.
    """

    "Parameters: [dataframe]: [time, joint_x, joint_y]"

    "Returns: [tuple]: horizontal velocity, vertical velocity,  [units]: m/s"

    def calculate_speed(self, data):

        if data.shape[1] != 3:
            print("DataFrame should have three columns.")
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
            vel = math.sqrt(math.pow(x, 2) + math.pow(y, 2))
            time.append(data.at[i, "time"])
            speed.append(vel)

        return time, speed
    
    """
    Description: [text]:
    Calculate the horizontal and vertical displacement using 2D coordinates, as well as the resultant displacement.
    First central defference method.
    """
    
    def calculate_displacement(self, data):
        
        if data.shape[1] != 3:
            print('Dataframe should have three columns.')
            return 1
        
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


class Energy:

    """
    Description: [text]:
    Estimates the energy expenditure based to velocity.
    Equation derives from 'Energy-speed relation and optimal speed during level walking (1958)' article.
    
    """

    "Parameters: [float]: [velocity], [units]: m/min"

    "Returns: [float]: [energy expenditure], [units]: cal/meter/kg"

    def energy_expenditure(self, velocity):
        e = 29 / velocity + 0.0053 * velocity
        return e
