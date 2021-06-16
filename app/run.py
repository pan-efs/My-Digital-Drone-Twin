from build import SkeletonTrackingApp
from exceptions.application import RunningError

if __name__ == '__main__':
    try:
        app = SkeletonTrackingApp()
        app.run()
    except Exception as ex:
        raise RunningError(ex)