import pandas as pd

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
                        converters = {1: converter, 
                                    2: converter, 
                                    3: converter}, 
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
        columns = ['joint_x', 'joint_y', 'joint_z']
        joint_0[columns] = joint_0[columns].fillna(method = 'ffill')
        joint_1[columns] = joint_1[columns].fillna(method = 'ffill')
        joint_2[columns] = joint_2[columns].fillna(method = 'ffill')
        joint_3[columns] = joint_3[columns].fillna(method = 'ffill')
        joint_4[columns] = joint_4[columns].fillna(method = 'ffill')
        joint_5[columns] = joint_5[columns].fillna(method = 'ffill')
        joint_6[columns] = joint_6[columns].fillna(method = 'ffill')
        joint_7[columns] = joint_7[columns].fillna(method = 'ffill')
        joint_8[columns] = joint_8[columns].fillna(method = 'ffill')
        joint_9[columns] = joint_9[columns].fillna(method = 'ffill')
        joint_10[columns] = joint_10[columns].fillna(method = 'ffill')
        joint_11[columns] = joint_11[columns].fillna(method = 'ffill')
        joint_12[columns] = joint_12[columns].fillna(method = 'ffill')
        joint_13[columns] = joint_13[columns].fillna(method = 'ffill')
        joint_14[columns] = joint_14[columns].fillna(method = 'ffill')
        joint_15[columns] = joint_15[columns].fillna(method = 'ffill')
        joint_16[columns] = joint_16[columns].fillna(method = 'ffill')
        joint_17[columns] = joint_17[columns].fillna(method = 'ffill')
        
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