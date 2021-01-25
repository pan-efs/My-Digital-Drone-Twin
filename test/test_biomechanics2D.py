from unittest import TestCase
import pandas as pd
from biomechanics.biomechanics2D import AngularKinematics as angular_kinematics
from biomechanics.biomechanics2D import LinearKinematics as linear_kinematics
from biomechanics.biomechanics2D import Energy as energy


class TestAngularKinematics(TestCase):
    def test_calculate_abs_angle(self):
        ang = angular_kinematics()
        knee = [1.22, 0.51]
        ankle = [1.09, 0.09]
        theta = ang.calculate_abs_angle(knee, ankle)
        self.assertEqual(72.80145877993417, theta)

    def test_calculate_rel_angle(self):
        ang = angular_kinematics()
        hip = [1.14, 0.80]
        knee = [1.22, 0.51]
        ankle = [1.09, 0.09]
        theta = ang.calculate_rel_angle(hip, knee, ankle)
        self.assertEqual(147.37929746119542, theta)


class TestLinearKinematics(TestCase):
    def test_calculate_velocity(self):
        k = linear_kinematics()
        data = [[0.0000, 0.00, 0.00], [0.0167, 0.10, 0.15], [0.0334, 0.12, 0.22], [0.0501, 0.15, 0.27], [0.0668, 0.15, 0.30], [0.0835, 0.18, 0.20]]
        df = pd.DataFrame(data, columns = ['time', 'joint_x', 'joint_y'])
        vel = k.calculate_velocity(df)
        vel_df = pd.DataFrame(data = vel)
        vel_df_T = vel_df.T
        vel_df_T = vel_df_T.rename(columns={0: 'time', 1: 'velocity_x', 2: 'velocity_y'})
        self.assertEqual(vel_df_T.at[0, 'time'], 0.0167)
        self.assertEqual(vel_df_T.at[2, 'velocity_y'], 2.395209580838323)
    
    def test_calculate_acceleration(self):
        k = linear_kinematics()
        data = [[0.0000, 0.00, 0.00], [0.0167, 0.10, 0.15], [0.0334, 0.12, 0.22], [0.0501, 0.15, 0.27], [0.0668, 0.15, 0.30], [0.0835, 0.18, 0.20]]
        df = pd.DataFrame(data, columns = ['time', 'joint_x', 'joint_y'])
        vel = k.calculate_velocity(df)
        vel_df = pd.DataFrame(data = vel)
        vel_df_T = vel_df.T
        vel_df_T = vel_df_T.rename(columns={0: 'time', 1: 'velocity_x', 2: 'velocity_y'})
        acc = k.calculate_acceleration(vel_df_T)
        acc_df = pd.DataFrame(data = acc)
        acc_df_T = acc_df.T
        acc_df_T = acc_df_T.rename(columns={0: 'time', 1: 'acceleration_x', 2: 'acceleration_y'})
        self.assertEqual(acc_df_T.at[0, 'time'], 0.0334)
        self.assertEqual(acc_df_T.at[1, 'acceleration_x'], -17.928215425436555)

class TestEnergy(TestCase):
    def test_energy_expenditure(self):
        en = energy()
        v = 40.2
        e = en.energy_expenditure(v)
        self.assertEqual(0.9344530348258706, e)
