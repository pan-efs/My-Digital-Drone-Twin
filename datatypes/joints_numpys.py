import numpy as np
import pandas as pd
from dataclasses import dataclass
from joints_dataframe import JointsDataframe

@dataclass
class JointsDfs:
    _joint0: pd.DataFrame
    _joint1: pd.DataFrame
    _joint2: pd.DataFrame
    _joint3: pd.DataFrame
    _joint4: pd.DataFrame 
    _joint5: pd.DataFrame
    _joint6: pd.DataFrame
    _joint7: pd.DataFrame
    _joint8: pd.DataFrame
    _joint9: pd.DataFrame
    _joint10: pd.DataFrame
    _joint11: pd.DataFrame
    _joint12: pd.DataFrame
    _joint13: pd.DataFrame
    _joint14: pd.DataFrame
    _joint15: pd.DataFrame
    _joint16: pd.DataFrame
    _joint17: pd.DataFrame

class JointsNumpys(JointsDfs):
    def __init__(self):
        [self._joint0, self._joint1, self._joint2, self._joint3, 
        self._joint4, self._joint5, self._joint6, self._joint7,
        self._joint8, self._joint9, self._joint10, self._joint11,
        self._joint12, self._joint13, self._joint14, self._joint15,
        self._joint16, self._joint17]                                = JointsDataframe().__repr__() 
    
    def __repr__(self):
        return self.__return_nps__()
    
    def __return_dfs__(self):
        ls = [self._joint0, self._joint1, self._joint2, self._joint3, 
                self._joint4, self._joint5, self._joint6, self._joint7,
                self._joint8, self._joint9, self._joint10, self._joint11,
                self._joint12, self._joint13, self._joint14, self._joint15,
                self._joint16, self._joint17]
        
        return ls
    
    def __return_nps__(self):
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
        :rtype: np.ndarray
        """
        arrX = joint_df['joint_x'].to_numpy()
        arrY = joint_df['joint_y'].to_numpy()
        arrZ = joint_df['joint_z'].to_numpy()
        
        return arrX, arrY, arrZ
