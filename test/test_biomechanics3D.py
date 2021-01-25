from unittest import TestCase
import pandas as pd
from biomechanics.biomechanics3D import LinearKinematics as linear_kinematics

class TestLinearKinematics(TestCase):
    
    def test_calculate_speed(self):
        k = linear_kinematics()
        data = [[0.0000, 0.00, 0.00, 0.00], [0.0167, 0.10, 0.15, 0.20], [0.0334, 0.12, 0.22, 0.28], [0.0501, 0.15, 0.27, 0.35]]
        df = pd.DataFrame(data = data, columns=['time', 'joint_x', 'joint_y', 'joint_z'])
        speed = k.calculate_speed(df)
        self.assertEqual([11.250475585662238, 5.942944084215331], speed)
    