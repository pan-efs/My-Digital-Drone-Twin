import pandas as pd
import numpy as np

from exceptions.movement_analysis import LengthArraysError

class JointsDataframe:
    def __init__(self, text_path: str, out_path: str):
        self.text_path = text_path
        self.out_path = out_path
        self.remove_brackets()
    
    def __str__(self):
        return f'The input text path is: {self.text_path} AND the output path is: {self.out_path}'
    
    def __repr__(self):
        return f'JointsDataframe(text_path={self.text_path}, out_path={self.out_path})'
    
    def __return__(self):
        return self._transformer()
    
    def _standarize(self):
        # Replace str NaNs with np.nan
        converter = lambda x: pd.to_numeric(x, 'coerce')
        
        df = pd.read_csv(self.out_path, delimiter = ",", 
                        converters = {
                                    1: converter, 
                                    2: converter, 
                                    3: converter
                                    }, 
                        header = None)
        std_df = self._rename(df)
        
        return std_df
    
    def _rename(self, df: pd.DataFrame):
        df = df.rename({
                        0: 'joint_index', 
                        1: 'joint_x',
                        2: 'joint_y',
                        3: 'joint_z'
                        },
                axis = 'columns')
        
        return df
    
    def _transformer(self):
        """
        Split the main dataframe into 18 distinct dataframes with x, y, z coordinates as columns.
        
        :return: From joint_0 to joint_17
        :rtype: DataFrame
        """
        df = self._standarize()
        
        # Split dataframe according to joint_index
        joint_0 = df.loc[df['joint_index'] == 0] # nose
        joint_1 = df.loc[df['joint_index'] == 1] # upper sternum
        joint_2 = df.loc[df['joint_index'] == 2] # upper body
        joint_3 = df.loc[df['joint_index'] == 3] # .
        joint_4 = df.loc[df['joint_index'] == 4] # .
        joint_5 = df.loc[df['joint_index'] == 5] # .
        joint_6 = df.loc[df['joint_index'] == 6] # .
        joint_7 = df.loc[df['joint_index'] == 7] # .
        joint_8 = df.loc[df['joint_index'] == 8] # lower body
        joint_9 = df.loc[df['joint_index'] == 9] # .
        joint_10 = df.loc[df['joint_index'] == 10] # .
        joint_11 = df.loc[df['joint_index'] == 11] # .
        joint_12 = df.loc[df['joint_index'] == 12] # .
        joint_13 = df.loc[df['joint_index'] == 13] #. 
        joint_14 = df.loc[df['joint_index'] == 14] # eyes
        joint_15 = df.loc[df['joint_index'] == 15] # .
        joint_16 = df.loc[df['joint_index'] == 16] # ears
        joint_17 = df.loc[df['joint_index'] == 17] #. 
        
        # Delete joint_index column as unnecessary
        del joint_0['joint_index']
        del joint_1['joint_index']
        del joint_2['joint_index']
        del joint_3['joint_index']
        del joint_4['joint_index']
        del joint_5['joint_index']
        del joint_6['joint_index']
        del joint_7['joint_index']
        del joint_8['joint_index']
        del joint_9['joint_index']
        del joint_10['joint_index']
        del joint_11['joint_index']
        del joint_12['joint_index']
        del joint_13['joint_index']
        del joint_14['joint_index']
        del joint_15['joint_index']
        del joint_16['joint_index']
        del joint_17['joint_index']
        
        # Fill np.nan values
        joint_0.interpolate()
        joint_1.interpolate()
        joint_2.interpolate()
        joint_3.interpolate()
        joint_4.interpolate()
        joint_5.interpolate()
        joint_6.interpolate()
        joint_7.interpolate()
        joint_8.interpolate()
        joint_9.interpolate()
        joint_10.interpolate()
        joint_11.interpolate()
        joint_12.interpolate()
        joint_13.interpolate()
        joint_14.interpolate()
        joint_15.interpolate()
        joint_16.interpolate()
        joint_17.interpolate()
        
        # Reset indexes
        joint_0 = joint_0.reset_index(drop=True)
        joint_1 = joint_1.reset_index(drop=True)
        joint_2 = joint_2.reset_index(drop=True)
        joint_3 = joint_3.reset_index(drop=True)
        joint_4 = joint_4.reset_index(drop=True)
        joint_5 = joint_5.reset_index(drop=True)
        joint_6 = joint_6.reset_index(drop=True)
        joint_7 = joint_7.reset_index(drop=True)
        joint_8 = joint_8.reset_index(drop=True)
        joint_9 = joint_9.reset_index(drop=True)
        joint_10 = joint_10.reset_index(drop=True)
        joint_11 = joint_11.reset_index(drop=True)
        joint_12 = joint_12.reset_index(drop=True)
        joint_13 = joint_13.reset_index(drop=True)
        joint_14 = joint_14.reset_index(drop=True)
        joint_15 = joint_15.reset_index(drop=True)
        joint_16 = joint_16.reset_index(drop=True)
        joint_17 = joint_17.reset_index(drop=True)
        
        return joint_0, joint_1, joint_2, joint_3, joint_4, joint_5, joint_6, joint_7, joint_8, joint_9, joint_10, joint_11, joint_12, joint_13, joint_14, joint_15, joint_16, joint_17
    
    def remove_brackets(self):
        """
        Clean an input text file from opening and closing brackets
        and save it in an output file.
        """
        fin = open(self.text_path, "rt")
        fout = open(self.out_path, "wt")
    
        for ln in fin:
            fout.write(ln.replace('[', '').replace(']', ''))
    
        fin.close()
        fout.close()

class JointsNumpys:
    def __init__(self, text_path: str, out_path: str):
        self.text_path = text_path
        self.out_path = out_path
        
        [self._joint0, self._joint1, self._joint2, self._joint3, 
        self._joint4, self._joint5, self._joint6, self._joint7,
        self._joint8, self._joint9, self._joint10, self._joint11,
        self._joint12, self._joint13, self._joint14, self._joint15,
        self._joint16, self._joint17]                                = JointsDataframe(self.text_path, self.out_path).__return__()
    
    def __str__(self):
        return f'The input text path is: {self.text_path} AND the output path is: {self.out_path}'
    
    def __repr__(self):
        return f'JointsNumpys(text_path={self.text_path}, out_path={self.out_path})'
    
    def __return__(self):
        return self.__return_nps__()
    
    def __return_dfs__(self):
        ls = [self._joint0, self._joint1, self._joint2, self._joint3, 
                self._joint4, self._joint5, self._joint6, self._joint7,
                self._joint8, self._joint9, self._joint10, self._joint11,
                self._joint12, self._joint13, self._joint14, self._joint15,
                self._joint16, self._joint17]
        
        return ls
    
    def __return_nps__(self):
        """
        Split each dataframe into a list which contains coordinates of x, y, z.
        
        :rtype: List
        """
        ls = self.__return_dfs__()
        
        converted_list = []
        
        for i in range(0, len(ls)):
            x, y, z = self._converter(ls[i])
            converted_list.append(x)
            converted_list.append(y)
            converted_list.append(z)
        
        return converted_list
    
    def _converter(self, joint_df: pd.DataFrame):
        """
        Converts each column of a JointsDataframe to array.
        
        :param joint_df: JointsDataframe dataframe
        :type joint_df: pd.DataFrame
        
        :return: Three arrays of X,Y,Z coordinates, respectively.
        :rtype: np.array
        """
        arrX = joint_df['joint_x'].to_numpy()
        arrY = joint_df['joint_y'].to_numpy()
        arrZ = joint_df['joint_z'].to_numpy()
        
        return arrX, arrY, arrZ

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
