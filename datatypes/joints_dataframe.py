import pandas as pd
from dataclasses import dataclass

@dataclass
class JointsText:
    #TODO: text_path should be derived from a config file. Then, delete the file from the folder.
    text_path: str = 'C:\\Users\\Drone\\Desktop\\Panagiotis\\My-Digital-Drone-Twin\\samples\\data\\standstill_mj.txt'
    out_path: str = 'C:\\Users\\Drone\\Desktop\\Panagiotis\\My-Digital-Drone-Twin\\datatypes\\clean\\clean_3d.txt'
    
class JointsDataframe(JointsText):
    def __init__(self):
        self.remove_brackets()
    
    def __repr__(self):
        return self._transformer()
    
    def _standarize(self):
        df = pd.read_csv(self.out_path, delimiter = ",", header = None)
        std_df = self._rename(df)
        
        return std_df
    
    def _rename(self, df: pd.DataFrame):
        df = df.rename({0: 'joint_index', 1: 'joint_x', 2: 'joint_y', 3: 'joint_z'},
                axis = 'columns')
        
        return df
    
    def _transformer(self):
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
        fin = open(self.text_path, "rt")
        fout = open(self.out_path, "wt")
    
        for ln in fin:
            fout.write(ln.replace('[', '').replace(']', ''))
    
        fin.close()
        fout.close()