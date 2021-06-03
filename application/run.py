from build import SkeletonTrackingApp

if __name__ == '__main__':
    try:
        app = SkeletonTrackingApp()
        app.run()
    except Exception as ex:
        print('Exception occured: "{}"'.format(ex))