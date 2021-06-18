import os, subprocess

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
retcode = subprocess.call('coverage run -m unittest discover && coverage report -m', shell = True)

if retcode == 0:
        print('Tests has been run successfully!')
else:
        raise RuntimeError