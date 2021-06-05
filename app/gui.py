from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget

import pyqtgraph as pg
import os
import sys
import subprocess

def _get_base_dir():
    if getattr(sys, 'frozen', False):
        BASE_DIR = os.path.dirname(sys.executable)
    else:
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    return BASE_DIR
class WelcomeScreen(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        
        self.setMinimumHeight(500)
        self.setMinimumWidth(500)
        self.setWindowTitle("Welcome!")
        self.main_style()
        
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
        button.clicked.connect(self.detected_button)
        button.clicked.connect(self.start_recording)
        boxlayout.addWidget(button)
        
        centralWidget.setLayout(boxlayout)
    
    def start_recording(self):
        msg_box = QMessageBox()
        msg_box.setText('Do you want to record hammer throw event?')
        msg_box.setInformativeText('No/X-cycling. Discard-just recording. Cancel-back.')
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.Discard | QMessageBox.Close | QMessageBox.Cancel)
        msg_box.setDefaultButton(QMessageBox.Yes)
        msg_box.setWindowTitle('Recording...')
        user_reply = msg_box.exec()
        
        msg_path = QMessageBox()
        msg_path.setText('Oops! Local path cannot be found.')
        msg_path.setIcon(QMessageBox.Warning)
        msg_path.setStandardButtons(QMessageBox.Ok)
        msg_path.setDefaultButton(QMessageBox.Ok)
        
        msg_dev = QMessageBox()
        msg_dev.setText('No device connected.')
        msg_dev.setIcon(QMessageBox.Warning)
        msg_dev.setStandardButtons(QMessageBox.Ok)
        msg_dev.setDefaultButton(QMessageBox.Ok)
        
        if user_reply == QMessageBox.Yes:
            try:
                BASE_DIR = _get_base_dir()
                os.chdir(BASE_DIR + '/cubemos')
                retcode = subprocess.call('python realsense.py', shell = True)
                
                if retcode == 0:
                    print('Go to hammer screen')
                    self.main_style()
                    self.switch_to_hammer_screen().show()
                else:
                    self.main_style()
                    raise RuntimeError
                
            except OSError:
                self.main_style()
                msg_path.exec()
            
            except RuntimeError:
                self.main_style()
                msg_dev.exec()
                
        elif user_reply == QMessageBox.Close:
            # TODO: Cycling screen if we include it
            try:
                BASE_DIR = _get_base_dir()
                os.chdir(BASE_DIR + '/cubemos')
                retcode = subprocess.call('python realsense.py', shell = True)
                
                if retcode == 0:
                    print('Go to cycling screen')
                    self.main_style()
                    #self.switch_to_cycling_screen().show()
                else:
                    self.main_style()
                    raise RuntimeError
                
            except OSError:
                self.main_style()
                msg_path.exec()
            
            except RuntimeError:
                self.main_style()
                msg_dev.exec()
                
        elif user_reply == QMessageBox.Discard:
            try:
                BASE_DIR = _get_base_dir()
                os.chdir(BASE_DIR + '/cubemos')
                retcode = subprocess.call('python realsense.py', shell = True)
                
                if retcode == 0:
                    print('Just recording')
                    self.main_style()
                else:
                    self.main_style()
                    raise RuntimeError
                
            except OSError:
                self.main_style()
                msg_path.exec()
            
            except RuntimeError:
                self.main_style()
                msg_dev.exec()
                
        elif user_reply == QMessageBox.Cancel:
            self.main_style()
    
    def switch_to_hammer_screen(self):
        self.hammer = HammerThrowScreen()
        return self.hammer
    
    def main_style(self):
        self.setStyleSheet('margin: 1px; padding: 10px; \
                            background-color: rgba(220, 245, 250, 0.5); \
                            color: rgba(0,0,0,255); \
                            border-style: solid; \
                            border-radius: 2px; border-width: 1px; \
                            border-color: rgba(0,0,0,255);')
    
    def detected_button(self):
        self.setStyleSheet('margin: 1px; padding: 10px; \
                            background-color: rgba(95, 200, 255, 0.5); \
                            color: rgba(0,0,0,255); \
                            border-style: solid; \
                            border-radius: 4px; border-width: 3px; \
                            border-color: rgba(0,0,0,255);')


class HammerThrowScreen(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        
        self.setMinimumHeight(900)
        self.setMinimumWidth(1700)
        self.setWindowTitle('Hammer Throw')
        self.setStyleSheet('background-color: rgba(220, 245, 250, 0.5);')
        
        try:
            self.BASE_DIR = _get_base_dir()
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
        self.combobox.addItem('None')
        self.combobox.addItem('Distances')
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
            
            pen_kn = pg.mkPen(color= 'r', width = 4)
            pen_an = pg.mkPen(color= 'b', width = 4)
            styles = {
                    'color': '#000000', 
                    'font-size': '20px',
                    }
            self.graphWidget.setLabel('left', 'meters', **styles)
            self.graphWidget.addLegend()
            self.graphWidget.setRange(xRange = (0, max(len(an_lines), len(an_lines))), yRange = (0, max(kn_lines)))
            self.graphWidget.plot(kn_lines, name = 'Knees', pen = pen_kn, symbol = 'x', symbolPen = pen_kn, symbolBrush = 0.3)
            self.graphWidget.plot(an_lines, name = 'Ankles', pen = pen_an, symbol = 'x', symbolPen = pen_an, symbolBrush = 0.3)
            
        elif txt == 'None':
            self.graphWidget.clear()