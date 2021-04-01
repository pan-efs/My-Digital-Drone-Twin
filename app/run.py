from build import MyDigitalDroneTwin
from exceptions.application import RunningError

try:
    MyDigitalDroneTwin().run()
except Exception as ex:
    raise RunningError(ex)