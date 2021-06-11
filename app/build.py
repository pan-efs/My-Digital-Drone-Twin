from gui import WelcomeScreen

from PyQt5.QtWidgets import *
import sys


class SkeletonTrackingApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
    
    def build(self):
        self.welcome = WelcomeScreen()
    
    def show(self):
        self.welcome.show()
    
    def run(self):
        self.build()
        self.show()
        sys.exit(self.app.exec_())