from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget

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
        msg_box.setText('For hammer throw press yes, otherwise no!')
        msg_box.setInformativeText('No means cycling.')
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
        
        self.setMinimumHeight(700)
        self.setMinimumWidth(1600)
        self.setWindowTitle('Hammer Throw')
        
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        video = QVideoWidget()
        
        centralwidget = QWidget(self)
        self.setCentralWidget(centralwidget) 
        
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
        
        self.lbl = QLabel()
        self.lbl.setText('Plot Distances')
        self.lbl.setAlignment(Qt.AlignCenter)
        
        self.combobox = QComboBox()
        self.combobox.addItem('Distances')
        self.combobox.addItem('Distances (Unfiltered)')
        self.combobox.currentTextChanged.connect(self.get_current_text)
        
        visLayout = QHBoxLayout()
        visLayout.addWidget(self.lbl)
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
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.mediaPlayer.setMedia(
                    QMediaContent(QUrl.fromLocalFile(BASE_DIR + '/cubemos' + '/output-skeleton.avi')))
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
    def get_current_text(self):
        txt = self.combobox.currentText()
        if txt == 'Distances':
            self.lbl.setText('Plot Distances')
        else:
            self.lbl.setText('Plot Positions')



if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    welcome = WelcomeScreen()
    
    welcome.show()
    
    sys.exit(app.exec_())