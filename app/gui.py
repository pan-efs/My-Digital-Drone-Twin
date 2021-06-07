from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget

import pyqtgraph as pg
import sys, os, subprocess

def _get_base_dir():
    frozen = 'not'
    if getattr(sys, 'frozen', False):
        frozen = 'ever so'
        BASE_DIR = sys._MEIPASS
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
        msg_box.setInformativeText('No-.bag, Discard-just recording. Cancel-back.')
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
        
        msg_lic = QMessageBox()
        msg_lic.setText('You do not have the permission to convert your file.')
        msg_lic.setIcon(QMessageBox.Warning)
        msg_lic.setStandardButtons(QMessageBox.Ok)
        msg_lic.setDefaultButton(QMessageBox.Ok)
        
        if user_reply == QMessageBox.Yes:
            try:
                BASE_DIR = _get_base_dir()
                os.chdir(BASE_DIR + '/cubemos')
                retcode = subprocess.call('python realsense.py', shell = True)
                
                if retcode == 0:
                    print('Go to screen for analysis after recording')
                    self.main_style()
                    self.switch_to_hammer_screen('Yes').show()
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
            try:
                BASE_DIR = _get_base_dir()
                os.chdir(BASE_DIR + '/cubemos_converter')
                retcode = subprocess.call('python convert_bagfile_skel.py', shell = True)
                
                if retcode == 0:
                    print('Go to converter screen')
                    self.switch_to_hammer_screen('No').show()
                    self.main_style()
                else:
                    self.main_style()
                    raise NotImplementedError
                
            except OSError:
                self.main_style()
                msg_path.exec()
            
            except NotImplementedError:
                self.main_style()
                msg_lic.exec()
                
        elif user_reply == QMessageBox.Discard:
            try:
                BASE_DIR = _get_base_dir()
                os.chdir(BASE_DIR + '/datatypes')
                retcode = subprocess.call('python hammer_example.py --file C:/Users/Drone/Desktop/Panagiotis/My-Digital-Drone-Twin/cubemos_converter/logging/get_3d_joints_from_video.txt', shell = True)
                
                if retcode == 0:
                    print('Text Analysis')
                    self.main_style()
                    self.switch_to_text_screen().show()
                else:
                    self.main_style()
                    raise NotImplementedError
                
            except OSError:
                self.main_style()
                msg_path.exec()
            
            except NotImplementedError:
                self.main_style()
                
        elif user_reply == QMessageBox.Cancel:
            self.main_style()
    
    def switch_to_hammer_screen(self, event:str):
        self.hammer = HammerThrowScreen(event)
        return self.hammer
    
    def switch_to_text_screen(self):
        self.text_screen = TextFileScreen()
        return self.text_screen
    
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
    def __init__(self, welcome_screen_event):
        QMainWindow.__init__(self)
        
        self.welcome_screen_event = welcome_screen_event
        
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
        
        self.open_video(self.welcome_screen_event)
    
    # Methods related to video playback
    def open_video(self, previous_screen_event: str):
        if previous_screen_event == 'Yes':
            format = '/cubemos'
        elif previous_screen_event == 'No':
            format = '/cubemos_converter'
        
        desired_dir = self.BASE_DIR + format
        desired_ext = '.avi'
        
        for i in os.listdir(desired_dir):
            if i.endswith(desired_ext):
                self.desired_path = i
                
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(self.desired_path)))
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
        # TODO: run hammer analysis script first, otherwise .txt files will not be modified.
        # if flag yes,...if flag no,...
        text_and_plot(self.BASE_DIR, self.graphWidget, self.combobox)

class TextFileScreen(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
            
        self.setMinimumHeight(900)
        self.setMinimumWidth(1700)
        self.setWindowTitle('Text Analysis')
        self.setStyleSheet('background-color: rgba(220, 245, 250, 0.5);')
        
        try:
            self.BASE_DIR = _get_base_dir()
        except OSError:
            raise NotImplementedError
        
        centralwidget = QWidget(self)
        self.setCentralWidget(centralwidget)
        
        self.graphWidget = pg.PlotWidget()
        self.graphWidget.setBackground('w')
        self.graphWidget.showGrid(x = True, y = True)
        
        self.combobox = QComboBox()
        self.combobox.addItem('None')
        self.combobox.addItem('Distances')
        self.combobox.currentTextChanged.connect(self.get_current_text_and_plot)
        
        visLayout = QHBoxLayout()
        visLayout.addWidget(self.graphWidget)
        visLayout.addWidget(self.combobox)
        
        centralwidget.setLayout(visLayout)
    
    def get_current_text_and_plot(self):
        # TODO: Get the text file from user not manually as now
        text_and_plot(self.BASE_DIR, self.graphWidget, self.combobox)







# Utilities
def text_and_plot(base_dir:str, graphWidget, combobox):
        txt = combobox.currentText()
        
        if txt == 'Distances':
            knees_dir = base_dir + '/datatypes/logging/knee_distances.txt'
            
            with open(knees_dir, 'r') as knees:
                kn_lines = knees.readlines()
            knees.close()
            
            for i in range(0, len(kn_lines)):
                kn_lines[i] = float(kn_lines[i][:-1])
            
            ankles_dir = base_dir + '/datatypes/logging/ankle_distances.txt'
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
            graphWidget.setLabel('left', 'meters', **styles)
            graphWidget.addLegend()
            graphWidget.setRange(xRange = (0, max(len(an_lines), len(an_lines))), yRange = (0, max(kn_lines)))
            graphWidget.plot(kn_lines, name = 'Knees', pen = pen_kn, symbol = 'x', symbolPen = pen_kn, symbolBrush = 0.3)
            graphWidget.plot(an_lines, name = 'Ankles', pen = pen_an, symbol = 'x', symbolPen = pen_an, symbolBrush = 0.3)
            
        elif txt == 'None':
            graphWidget.clear()