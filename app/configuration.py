import json
from exceptions.application import ReadingConfigurationError, IndexConfigurationError

class Configuration:
    def __init__(self):
        self.config = {
            "main": "C:\\Users\\Drone\\Desktop\\Panagiotis\\My-Digital-Drone-Twin\\",
            "realsense_viewer": "C:\\Users\\Public\\Desktop\\Intel RealSense Viewer.lnk",
            "skeletal_tracking": "C:\\Users\\Drone\\Desktop\\Panagiotis\\Cycling data\\20210218_113139.bag",
            "offline_analysis": "C:\\Users\\Drone\\Desktop\\Panagiotis\\Cycling data\\20210218_113139both.avi"
        }
    
    # This function should replace self.config in the future.
    def _read_settings(self):
        self.config_list = []
        
        try:
            with open("logging\\settings.txt", "r") as f:
                path = f.readlines()
                for i in range(0, len(path)):
                    path[i] = path[i][:-1]
                    self.config_list.append(path[i])
            return self.config_list
        
        except Exception as ex:
            raise ReadingConfigurationError(ex)
    
    def _config_json(self, config_list: list):
        try:
            self._json = {
                'main': config_list[3],
                'realsense_viewer': config_list[4],
                'skeletal_tracking': config_list[5],
                'offline_analysis': config_list[6]
            }
        except Exception as ex:
            raise IndexConfigurationError(ex)
        
        return self._json
    
    def _get_dir(self, key_path: str):
        return self.config[key_path]


#TODO: Write camera's configurations here as well.
#Comment: settings.txt should have at least 3 lines in order to run. Otherwise raises an error.