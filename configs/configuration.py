import json

class Configuration:
    
    def __init__(self):
        self.config = {
            "main": "C:\\Users\\Drone\\Desktop\\Panagiotis\\My-Digital-Drone-Twin\\",
            "realsense_viewer": "C:\\Users\\Public\\Desktop\\Intel RealSense Viewer.lnk",
            "offline_analysis": "C:\\Users\\Drone\\Desktop\\Panagiotis\\Moving camera\\standstill_martin.avi"
        }
    
    def _get_dir(self, key_path: str):
        return self.config[key_path]


#TODO: Write camera's configurations here as well.
