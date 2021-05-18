import json
from exceptions.application import ReadingConfigurationError, IndexConfigurationError

class Configuration:
    def __init__(self):
        self.config = {
            "main": "C:\\Users\\Drone\\Desktop\\Panagiotis\\My-Digital-Drone-Twin\\",
            "realsense_viewer": "C:\\Users\\Public\\Desktop\\Intel RealSense Viewer.lnk",
            "offline_analysis": "C:\\Users\\Drone\\Desktop\\Panagiotis\\Field\\20210416_134949.bag"
        }
        # In case of app running
        """ read_settings = self._read_settings()
        dict_settings = self._config_json(read_settings)
        self.config = dict_settings """
    
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
        length = len(config_list)
        
        try:
            self._json = {
                'main': config_list[length - 3],
                'realsense_viewer': config_list[length - 2],
                'offline_analysis': config_list[length - 1],
            }
        except Exception as ex:
            raise IndexConfigurationError(ex)
        
        return self._json
    
    def _get_dir(self, key_path: str):
        return self.config[key_path]