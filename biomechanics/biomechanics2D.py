import pandas as pd
import numpy as np
import math


class AngularKinematics:
    """
    Description: [text]:
    Calculates the absolute angle of a body segment on 2D saggital plane
    relative to right horizontal.
    
    """

    "Parameters: [joints]: proximal(x1,y1), distal(x2,y2)"

    "Returns: [type]: [angle in degrees]"

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
    "Parameters: [joints]: proximal(x1,y1), center(x2,y2), distal(x3,y3)"

    "Returns: [type]: [angle in degrees]"

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
    Calculates the hip angle using absolute angles.
    The right side of the subject's body is closest to the camera and is considered to 
    be in the x-y plane.
    
    """
    "Parameters: [absolute angles]: absolute_angle_thigh, absolute_angle_trunk"

    "Returns: [type]: [angle in degrees]"

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

    "Returns: [type]: [angle in degrees]"

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

    "Returns: [type]: [angle in degrees]"

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
    Calculates acceleration for horizontal and vertical components using the first central difference method.
    Acceleration is calculated between two video frames.
    Pre-requisite: analyze a video offline knowing in before fps.
    
    """
    "Parameters: [dataframe]: [time, velocity_x, velocity_y]"

    "Returns: [tuple]: horizontal acceleration, vertical acceleration,  [units]: m/s^2"

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

        return acc_x, acc_y


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