import numpy as np
from matplotlib import pyplot as plt

class Stats_utils:
    def __init__(self):
        return
    
    def standard_deviation(self, ls: list):
        arr = np.array(ls)
        std_dev = np.std(arr)
        std_dev = int(std_dev*100)/100
        
        return std_dev
    
    def variance(self, ls: list):
        arr = np.array(ls)
        var = np.var(arr)
        var = int(var*100)/100
        
        return var
    
    def maximum(self, ls: list):
        maxim = max(ls)
        maxim = int(maxim*100)/100
        
        return maxim
    
    def minimum(self, ls: list):
        minim = min(ls)
        minim = int(minim*100)/100
        
        return minim
    
    def mean(self, ls: list):
        arr = np.array(ls)
        avg = np.mean(arr)
        avg = int(avg*100)/100
        
        return avg
    
    def percentile(self, ls: list):
        arr = np.array(ls)
        per = np.percentile(arr, [5, 25, 50, 75, 90, 99])
        
        for i in range(0, len(per)):
            per[i] = int(per[i]*100)/100
        
        return per
    
    def stats_log(self, ls: list):
        std_dev = self.standard_deviation(ls)
        var = self.variance(ls)
        minim = self.minimum(ls)
        mean = self.mean(ls)
        maxim = self.maximum(ls)
        per = self.percentile(ls)
        
        log = {'min': minim, 'mean': mean, 'max': maxim, 'std_dev': std_dev, 'variance': var}
        
        return log, per
    
    def visualization(self, r_log: dict, l_log: dict,
                    r_title: str, l_title: str):
        fig, (ax0, ax1) = plt.subplots(1,2)
        ax0.bar(*zip(*r_log.items()))
        ax0.set_title(r_title)
        ax0.set(ylabel = 'Degrees')

        ax1.bar(*zip(*l_log.items()))
        ax1.set_title(l_title)

        plt.show()