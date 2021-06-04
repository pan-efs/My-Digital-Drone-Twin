from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from pyqtgraph import PlotWidget, plot

import pyqtgraph as pg
import os
import sys

class WelcomeScreen(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        
        self.setFixedHeight(500)
        self.setFixedWidth(500)    
        self.setWindowTitle("Welcome!")
        
        centralWidget = QWidget(self)          
        self.setCentralWidget(centralWidget) 
        
        boxlayout = QBoxLayout(QBoxLayout.TopToBottom)
        
        lbl_welcome = QLabel(centralWidget)
        lbl_welcome.setText('Welcome to Skeleton Tracking App!')
        lbl_welcome.setAlignment(Qt.AlignCenter)
        boxlayout.addWidget(lbl_welcome)
        
        lbl_instructions = QLabel(centralWidget)
        lbl_instructions.setText(
                        '1. Connect your Intel RealSense camera before start recording! \n' +
                        '2. Camera should be fixed. \n' +
                        '3. Press start recording and choose your movement. \n' +
                        '4. Press Esc button to stop recording.'
                        )
        lbl_instructions.setAlignment(Qt.AlignCenter)
        boxlayout.addWidget(lbl_instructions)
        
        button = QPushButton('Start Recording...')
        button.clicked.connect(self.start_recording)
        boxlayout.addWidget(button)
        
        centralWidget.setLayout(boxlayout)
    
    def start_recording(self):
        msg_box = QMessageBox()
        msg_box.setText('Do you want to record hammer throw event?')
        msg_box.setInformativeText('No means cycling. Close this window for just recording.')
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
        msg_box.setDefaultButton(QMessageBox.Yes)
        user_reply = msg_box.exec()
        
        msg_path = QMessageBox()
        msg_path.setText('Oops! Path cannot be found.')
        msg_path.setIcon(QMessageBox.Warning)
        msg_path.setStandardButtons(QMessageBox.Ok)
        msg_path.setDefaultButton(QMessageBox.Ok)
        
        if user_reply == QMessageBox.Yes:
            try:
                BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                os.chdir(BASE_DIR + '/cubemos')
                os.system('python realsense.py')
                print('Go to hammer screen')
                self.switch_to_hammer_screen().show()
                
            except OSError:
                msg_path.exec()
        else:
            try:
                BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                os.chdir(BASE_DIR + '/cubemos')
                os.system('python realsense.py')
                print('Go to cycling screen')
                # When we finish hammer screen, we copy it for cycling as well. It'll be almost the same code.
            except OSError:
                msg_path.exec()
    
    def switch_to_hammer_screen(self):
        self.hammer = HammerThrowScreen()
        return self.hammer


class HammerThrowScreen(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        
        self.setMinimumHeight(900)
        self.setMinimumWidth(1700)
        self.setWindowTitle('Hammer Throw')
        
        try:
            self.BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        except OSError:
            raise NotImplementedError
        
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        video = QVideoWidget()
        
        centralwidget = QWidget(self)
        self.setCentralWidget(centralwidget)
        
        self.graphWidget = pg.PlotWidget()
        self.graphWidget.setBackground('w')
        self.graphWidget.showGrid(x = True, y = True)
        self.graphWidget.setMaximumHeight(450)
        
        self.playButton = QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)

        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderMoved.connect(self.setPosition)
        
        controlLayout = QHBoxLayout()
        controlLayout.addWidget(self.playButton)
        controlLayout.addWidget(self.positionSlider)
        
        self.combobox = QComboBox()
        self.combobox.addItem('Distances')
        self.combobox.addItem('Distances (Unfiltered)')
        self.combobox.currentTextChanged.connect(self.get_current_text_and_plot)
        
        visLayout = QHBoxLayout()
        visLayout.addWidget(self.graphWidget)
        visLayout.addWidget(self.combobox)
        
        qvboxlayout = QVBoxLayout()
        qvboxlayout.addWidget(video)
        qvboxlayout.addLayout(controlLayout)
        qvboxlayout.addLayout(visLayout)
        
        centralwidget.setLayout(qvboxlayout)
        
        self.mediaPlayer.setVideoOutput(video)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        
        self.open_video()
    
    # Methods related to video playback
    def open_video(self):
        self.mediaPlayer.setMedia(
                    QMediaContent(QUrl.fromLocalFile(self.BASE_DIR + '/cubemos' + '/output-skeleton.avi')))
        self.playButton.setEnabled(True)
        
    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()
    
    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)
    
    def mediaStateChanged(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPlay))

    def positionChanged(self, position):
        self.positionSlider.setValue(position)

    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)
    
    # Methods related to visualization
    def get_current_text_and_plot(self):
        txt = self.combobox.currentText()
        
        # TODO: run hammer analysis script first, otherwise .txt files will not be modified.
        
        if txt == 'Distances':
            knees_dir = self.BASE_DIR + '/datatypes/logging/knee_distances.txt'
            
            with open(knees_dir, 'r') as knees:
                kn_lines = knees.readlines()
            knees.close()
            
            for i in range(0, len(kn_lines)):
                kn_lines[i] = float(kn_lines[i][:-1])
            
            ankles_dir = self.BASE_DIR + '/datatypes/logging/ankle_distances.txt'
            with open(ankles_dir, 'r') as ankles:
                an_lines = ankles.readlines()
            ankles.close()
            
            for i in range(0, len(an_lines)):
                an_lines[i] = float(an_lines[i][:-1])
            
            pen_kn = pg.mkPen(color= 'r')
            pen_an = pg.mkPen(color= 'b')
            styles = {
                    'color': '#000000', 
                    'font-size': '20px',
                    }
            self.graphWidget.setLabel('left', 'meters', **styles)
            self.graphWidget.addLegend()
            self.graphWidget.setRange(xRange = (0, max(len(an_lines), len(an_lines))), yRange = (0, max(kn_lines)))
            self.graphWidget.plot(kn_lines, name = 'Knees', pen = pen_kn)
            self.graphWidget.plot(an_lines, name = 'Ankles', pen = pen_an)
        else:
            self.lbl.setText('Plot Positions')



if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    welcome = WelcomeScreen()
    
    welcome.show()
    
    sys.exit(app.exec_())