import json

from exceptions.application import ReadingConfigurationError, IndexConfigurationError

class Configuration:
    def __init__(self):
        self.config = {
            "main": "C:\\Users\\Drone\\Desktop\\Panagiotis\\My-Digital-Drone-Twin\\",
            "realsense_viewer": "C:\\Users\\Public\\Desktop\\Intel RealSense Viewer.lnk",
            "offline_analysis": "C:\\Users\\Drone\\Desktop\\Panagiotis\\Moving camera\\standstill_martin.avi"
        }
    
    # This function should replace self.config in the future.
    def _read_settings(self):
        self.config_list = ['Not provided', 'Not provided', 'Not provided']
        
        try:
            with open("settings.txt", "r") as f:
                path = f.readlines()
                for i in range(0, len(path)):
                    path[i] = path[i][:-2]
                    self.config_list.append(path[i])
            return self.config_list
        
        except Exception as ex:
            raise ReadingConfigurationError(ex)
    
    def _config_json(self, config_list: list):
        try:
            self._json = {
                'main': config_list[5],
                'realsense_viewer': config_list[4],
                'offline_analysis': config_list[3]
            }
        except Exception as ex:
            raise IndexConfigurationError(ex)
        
        return self._json
    
    def _get_dir(self, key_path: str):
        return self.config[key_path]


#TODO: Write camera's configurations here as well.
#Comment: settings.txt should have at least 3 lines in order to run. Otherwise raises an error.