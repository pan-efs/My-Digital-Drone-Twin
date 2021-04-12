import psutil
import platform

class ComputerInfo:
    def __init__(self):
        pass
    
    def systems_info(self):
        print("="*40, "System Information", "="*40)
        self.uname = platform.uname()
        print(f"System: {self.uname.system}")
        print(f"Node Name: {self.uname.node}")
        print(f"Release: {self.uname.release}")
        print(f"Version: {self.uname.version}")
        print(f"Machine: {self.uname.machine}")
        print(f"Processor: {self.uname.processor}")

    def cpu_info(self):
        print("="*40, "CPU Info", "="*40)
        # number of cores
        print("Physical cores:", psutil.cpu_count(logical=False))
        print("Total cores:", psutil.cpu_count(logical=True))
        
        cpufreq = psutil.cpu_freq()
        print(f"Max Frequency: {cpufreq.max:.2f}Mhz")
        print(f"Min Frequency: {cpufreq.min:.2f}Mhz")
        print(f"Current Frequency: {cpufreq.current:.2f}Mhz")

        # CPU usage
        print("CPU Usage Per Core:")
        for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval = 1)):
            print(f"Core {i}: {percentage}%")
        
        print(f"Total CPU Usage: {psutil.cpu_percent()}%")
    
    def cpu_percent_utilization(self, interval = 0.1):
        print(f"Total CPU Usage: {psutil.cpu_percent(interval)}%")
    
    def _print_all_processes(self):
        for proc in psutil.process_iter(['pid', 'name', 'username']):
            print(proc.info)
    
    def get_cpu_percent_by_pid(self, pid, interval = 0.1):
        try:
            proc = psutil.Process(pid)
            tmp_val = proc.cpu_percent(interval)
        except psutil.NoSuchProcess:
            tmp_val = 0
        
        print(f'Total Process CPU Usage: {tmp_val}%')
        return tmp_val

