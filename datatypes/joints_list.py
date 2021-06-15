import numpy as np
from exceptions.movement_analysis import LengthArraysError
from joints_numpys import JointsNumpys

class JointsList:
    def __init__(self, text_path: str, out_path: str):
        self.text_path = text_path
        self.out_path = out_path
        
        [self.arr_0x, self.arr_0y, self.arr_0z,
        self.arr_1x, self.arr_1y, self.arr_1z,
        self.arr_2x, self.arr_2y, self.arr_2z,
        self.arr_3x, self.arr_3y, self.arr_3z,
        self.arr_4x, self.arr_4y, self.arr_4z,
        self.arr_5x, self.arr_5y, self.arr_5z,
        self.arr_6x, self.arr_6y, self.arr_6z,
        self.arr_7x, self.arr_7y, self.arr_7z,
        self.arr_8x, self.arr_8y, self.arr_8z,
        self.arr_9x, self.arr_9y, self.arr_9z,
        self.arr_10x, self.arr_10y, self.arr_10z,
        self.arr_11x, self.arr_11y, self.arr_11z,
        self.arr_12x, self.arr_12y, self.arr_12z,
        self.arr_13x, self.arr_13y, self.arr_13z,
        self.arr_14x, self.arr_14y, self.arr_14z,
        self.arr_15x, self.arr_15y, self.arr_15z,
        self.arr_16x, self.arr_16y, self.arr_16z,
        self.arr_17x, self.arr_17y, self.arr_17z] = JointsNumpys(self.text_path, self.out_path).__return__()
    
    def __str__(self):
        return f'The input text path is: {self.text_path} AND the output path is: {self.out_path}'
    
    def __repr__(self):
        return f'JointsList(text_path={self.text_path}, out_path={self.out_path})'
    
    def __return__(self):
        return self.__return_all__()
    
    def __return_all__(self):
        return [self.arr_0x, self.arr_0y, self.arr_0z,
                self.arr_1x, self.arr_1y, self.arr_1z,
                self.arr_2x, self.arr_2y, self.arr_2z,
                self.arr_3x, self.arr_3y, self.arr_3z,
                self.arr_4x, self.arr_4y, self.arr_4z,
                self.arr_5x, self.arr_5y, self.arr_5z,
                self.arr_6x, self.arr_6y, self.arr_6z,
                self.arr_7x, self.arr_7y, self.arr_7z,
                self.arr_8x, self.arr_8y, self.arr_8z,
                self.arr_9x, self.arr_9y, self.arr_9z,
                self.arr_10x, self.arr_10y, self.arr_10z,
                self.arr_11x, self.arr_11y, self.arr_11z,
                self.arr_12x, self.arr_12y, self.arr_12z,
                self.arr_13x, self.arr_13y, self.arr_13z,
                self.arr_14x, self.arr_14y, self.arr_14z,
                self.arr_15x, self.arr_15y, self.arr_15z,
                self.arr_16x, self.arr_16y, self.arr_16z,
                self.arr_17x, self.arr_17y, self.arr_17z]
    
    def _converter_to_list(self, arr_x: np.ndarray, arr_y: np.ndarray, arr_z: np.ndarray):
        """
        Helper function.
        Converts three arrays of x,y,z codrdinates into list.
        It can be applied only to unfiltered coordinates.

        :param arr_x: x joint position
        :param arr_y: y joint position
        :param arr_z: z joint position
        
        :raises LengthArraysError: See exceptions.movement_analysis.py
        
        :rtype: List
        """
        if (len(arr_x) != len(arr_y)) or (len(arr_x) != len(arr_z)) or (len(arr_y) != len(arr_z)):
            raise LengthArraysError()
        
        xyz = []
        
        for i in range(0, len(arr_x)):
            ls = [arr_x[i], arr_y[i], arr_z[i]]
            xyz.append(ls)
        
        return xyz
    
    def _get_same_length(self, arr1, arr2, arr3):
        len1 = len(arr1)
        len2 = len(arr2)
        len3 = len(arr3)
        min_len = min(len1, len2, len3)
    
        arr1 = arr1[:min_len]
        arr2 = arr2[:min_len]
        arr3 = arr3[:min_len]
        
        return arr1, arr2, arr3
