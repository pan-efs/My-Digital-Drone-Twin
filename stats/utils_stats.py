import numpy as np
from scipy.stats import norm, stats
from matplotlib import pyplot as plt

class StatsUtils:
    def __init__(self):
        return
    
    def _standard_deviation(self, ls: list):
        arr = np.array(ls)
        std_dev = np.std(arr)
        std_dev = int(std_dev*100)/100
        
        return std_dev
    
    def _variance(self, ls: list):
        arr = np.array(ls)
        var = np.var(arr)
        #var = int(var*100)/100
        
        return var
    
    def _maximum(self, ls: list):
        maxim = max(ls)
        maxim = int(maxim*100)/100
        
        return maxim
    
    def _minimum(self, ls: list):
        minim = min(ls)
        minim = int(minim*100)/100
        
        return minim
    
    def _mean(self, ls: list):
        arr = np.array(ls)
        avg = np.mean(arr)
        avg = int(avg*100)/100
        
        return avg
    
    def _median(self, ls: list):
        arr = np.array(ls)
        med = np.median(arr)
        med = int(med*100)/100
        
        return med
    
    def _mode(self, ls: list):
        arr = np.array(ls)
        mode_result = stats.mode(arr)
        _mode = int(mode_result.mode[0]*100)/100
        _count = int(mode_result.count[0]*100)/100
        
        return _mode, _count
    
    def _percentile(self, ls: list):
        arr = np.array(ls)
        per = np.percentile(arr, [5, 25, 50, 75, 90, 99])
        
        for i in range(0, len(per)):
            per[i] = int(per[i]*100)/100
        
        return per
    
    def _cdf(self, ls:list):
        "It works the same as 'percentile' function. Yet, it returns the probability for each value."
        x = np.array(ls)
        std_dev = self._standard_deviation(ls)
        mean = self._mean(ls)
        
        cdf = norm.cdf(x, mean, std_dev)
        
        return cdf
    
    def _pdf(self, ls:list):
        x = np.array(ls)
        std_dev = self._standard_deviation(ls)
        mean = self._mean(ls)
        
        pdf = norm.pdf(x, mean, std_dev)
        
        return pdf
    
    def stats_log(self, ls: list):
        std_dev = self._standard_deviation(ls)
        var = self._variance(ls)
        minim = self._minimum(ls)
        mean = self._mean(ls)
        median = self._median(ls)
        mode, count = self._mode(ls)
        maxim = self._maximum(ls)
        per = self._percentile(ls)
        
        log = {
            'min': minim, 
            'mean': mean,
            'median': median,
            'max': maxim, 
            'mode': mode,
            'std_dev': std_dev, 
            'variance': var
            }
        
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