import os
import platform
import time

class CubemosClass:
    """
    Description: [text]:
    Finds the default directory for cubemos license file.
    """
    def default_license_dir(self):
        platform == platform.system()
        
        if platform == "Windows":
            return os.path.join(os.environ["LOCALAPPDATA"], "Cubemos", "SkeletonTracking", "licence")
        else:
            raise Exception("{} is not supported".format(platform))
    
    
    """
    Description: [text]:
    Finds the default directory for cubemos log file.
    """
    def default_log_dir(self):
        platform == platform.system()
        
        if platform == "Windows":
            return os.path.join(os.environ["LOCALAPPDATA"], "Cubemos", "SkeletonTracking", "logs")
        else:
            raise Exception("{} is not supported".format(platform))
    
    """
    Description: [text]:
    A common phenomenon is that 'cubemos_license.json' file does not exists 
    due to installation errors by client.
    Thus, it looks if the aforementioned file exist in the default path.
    """
    def check_license_file(self):
        license_path = os.path.join(self.default_license_dir(), "cubemos_license.json")
        
        if os.path.isfile(license_path):
            return print("cubemos_license.json file exists!")
        else:
            raise Exception(
                "The license file has not been found in default path" +
                self.default_license_dir()
            )
