import pandas as pd
from joints_dataframe import JointsDataframe

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
