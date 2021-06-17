import os
from unittest import TestCase
from pandas import DataFrame

from datatypes.joints import JointsDataframe, JointsNumpys, JointsList

# Initialization of the paths
try:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_path = f'{BASE_DIR}/test/data/prerecorded_joints.txt'
    output_path = f'{BASE_DIR}/test/data/modified_joints.txt'
except Exception as ex:
    print('Exception occured: "{}"'.format(ex))
    raise ex

class TestJointsDatatype(TestCase):
    
    def test_dataframes(self):
        dfs = JointsDataframe(input_path, 
                                    output_path).__return__()
        
        self.assertEqual(len(dfs), 18)
        
        for i in range(0, 17):
            self.assertTrue(type(dfs[i]) is DataFrame)
            self.assertTrue(len(dfs[i].columns) == 3)
            
            if dfs[i].isnull().sum().sum() != 0:
                self.assertEqual(dfs[i].isnull().sum().sum(), 3*len(dfs[i])) # it's empty
            else:
                self.assertEqual(dfs[i].isnull().sum().sum(), 0) # filtering has been applied
    
    def test_numpys(self):
        ls = JointsNumpys(input_path, 
                                output_path).__return__()
        
        self.assertEqual(len(ls), 54)
        self.assertTrue(type(ls) is list)

        for i in range(0, 54, 3):
            self.assertEqual(len(ls[i]), len(ls[i+1]), len(ls[i+2]))
    
    def test_list(self):
        ls = JointsList(input_path, 
                                output_path).__return__()
        
        self.assertEqual(len(ls), 54)
        