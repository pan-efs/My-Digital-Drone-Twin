import numpy as np

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