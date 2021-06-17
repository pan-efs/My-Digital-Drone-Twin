from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget

from utils import (_get_base_dir, add_line, plot_cases, 
                    graph_length, radiobutton_toggled)

import pyqtgraph as pg
import os, subprocess

class WelcomeScreen(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        
        self.setMinimumHeight(500)
        self.setMinimumWidth(500)
        self.setWindowTitle("Welcome!")
        self.main_style()
        
        try:
            self.BASE_DIR = _get_base_dir()
        except OSError:
            raise NotImplementedError
        
        centralWidget = QWidget(self)          
        self.setCentralWidget(centralWidget) 
        
        boxlayout = QBoxLayout(QBoxLayout.TopToBottom)
        
        lbl_welcome = QLabel(centralWidget)
        lbl_welcome.setText('<big><b>Welcome to Skeleton Tracking App!</b></big>')
        lbl_welcome.setAlignment(Qt.AlignCenter)
        boxlayout.addWidget(lbl_welcome)
        
        lbl_instructions = QLabel(centralWidget)
        lbl_instructions.setText(
                        '<ol>1. Connect your camera if you intend to recording!</ol>' + 
                        '<ol>2. Camera should be fixed (recommendation).</ol>' +
                        '<ol>3. Press Esc button to stop recording.</ol>' +
                        '<ol>4. Choose your desired action from following list.</ol>'
                    )
        lbl_instructions.setAlignment(Qt.AlignCenter)
        boxlayout.addWidget(lbl_instructions)
        
        self.start_box = QComboBox()
        self.start_box.addItem('Choose your next movement...')
        self.start_box.addItem('Recording')
        self.start_box.addItem('Convert video')
        self.start_box.addItem('Text analysis')
        self.start_box.activated.connect(self.start_doing)
        boxlayout.addWidget(self.start_box)
        
        centralWidget.setLayout(boxlayout)
    
    def start_doing(self):
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
        msg_lic.setText('You do not have the permission to convert your file.\nOR \nCouldn\'t resolve requests.')
        msg_lic.setIcon(QMessageBox.Warning)
        msg_lic.setStandardButtons(QMessageBox.Ok)
        msg_lic.setDefaultButton(QMessageBox.Ok)
        
        msg_format = QMessageBox()
        msg_format.setText('The format of the file is not correct.')
        msg_format.setIcon(QMessageBox.Warning)
        msg_format.setStandardButtons(QMessageBox.Ok)
        msg_format.setDefaultButton(QMessageBox.Ok)
        
        user_reply = self.start_box.currentText()
        
        if user_reply == 'Recording':
            try:
                os.chdir(f'{self.BASE_DIR}/cubemos')
                retcode = subprocess.call('python realsense.py', shell = True)
                
                if retcode == 0:
                    print('Go to screen for analysis after recording')
                    self.switch_to_video_screen('Yes').show()
                else:
                    raise RuntimeError
                
            except OSError:
                msg_path.exec()
            
            except RuntimeError:
                msg_dev.exec()
                
        elif user_reply == 'Convert video':
            options = QFileDialog.Options()
            fileName, _ = QFileDialog.getOpenFileName(self,
                                                    "QFileDialog.getOpenFileName()","","All Files (*);;Bag Files (*.bag)", 
                                                    options = options)
            try:
                if fileName.endswith('.bag'):
                    print(fileName)
                    pass
                elif fileName == '':
                    raise NotImplementedError
                else:
                    raise FileNotFoundError
                
                os.chdir(f'{self.BASE_DIR}/cubemos_converter')
                retcode = subprocess.call(f'python convert_bagfile_skel.py --file {fileName}', shell = True)
                
                if retcode == 0:
                    print('Go to converter screen')
                    self.switch_to_video_screen('No').show()
                else:
                    raise RuntimeError
            
            except NotImplementedError:
                pass
            
            except RuntimeError:
                msg_lic.exec()
            
            except FileNotFoundError:
                msg_format.exec()
            
            except OSError:
                msg_path.exec()
            
                
        elif user_reply == 'Text analysis':
            options = QFileDialog.Options()
            fileName, _ = QFileDialog.getOpenFileName(self,
                                                    "QFileDialog.getOpenFileName()","","All Files (*);;Text Files (*.txt)", 
                                                    options = options)
            try:
                if fileName.endswith('.txt'):
                    print(fileName)
                    pass
                elif fileName == '':
                    raise NotImplementedError
                else:
                    raise FileNotFoundError
                
                os.chdir(f'{self.BASE_DIR}/datatypes')
                retcode = subprocess.call(f'python processing.py --file {fileName}', shell = True)
                
                if retcode == 0:
                    print('Text Analysis')
                    self.switch_to_text_screen().show()
            
            except FileNotFoundError:
                msg_format.exec()
            
            except OSError:
                msg_path.exec()
            
            except NotImplementedError:
                pass
            
        elif user_reply == 'Choose your next movement...':
            pass
    
    def switch_to_video_screen(self, event: str):
        self.hammer = VideoAnalysisScreen(event)
        return self.hammer
    
    def switch_to_text_screen(self):
        self.text_screen = TextFileScreen()
        return self.text_screen
    
    def main_style(self):
        self.setStyleSheet('margin: 1px; padding: 10px; \
                            background-color: rgba(171, 198, 228, 0.5); \
                            color: rgba(0,0,0,255); \
                            border-style: solid; \
                            border-radius: 2px; border-width: 1px; \
                            border-color: rgba(0,0,0,255);')

class VideoAnalysisScreen(QMainWindow):
    def __init__(self, welcome_screen_event):
        QMainWindow.__init__(self)
        
        self.welcome_screen_event = welcome_screen_event
        
        self.setMinimumHeight(900)
        self.setMinimumWidth(1700)
        self.setWindowTitle('Video analysis')
        self.setStyleSheet('background-color: rgba(171, 198, 228, 0.5);')
        
        try:
            self.BASE_DIR = _get_base_dir()
        except OSError:
            raise NotImplementedError
        
        self.index_analysis = 0
        self.initial_frames = graph_length(self.BASE_DIR, self.welcome_screen_event)
        self.frames = self.initial_frames - 6
        
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        video = QVideoWidget()
        
        centralwidget = QWidget(self)
        self.setCentralWidget(centralwidget)
        
        self.graphWidget = pg.PlotWidget()
        self.graphWidget.setBackground('w')
        self.graphWidget.showGrid(x = True, y = True)
        self.graphWidget.setMaximumHeight(450)
        self.line = 0
        
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
        self.combobox.addItem('Knees Magnitude')
        self.combobox.addItem('Ankles Magnitude')
        self.combobox.currentTextChanged.connect(self.get_current_text_and_plot)
        
        self.radioButtonThree = QRadioButton('3')
        self.radioButtonSix = QRadioButton('6')
        self.radioButtonNine = QRadioButton('9')
        self.radioButtonTwelve = QRadioButton('12')
        self.radioButtonSix.setChecked(True)
        self.radioButtonThree.pressed.connect(self.button_toggled)
        self.radioButtonSix.pressed.connect(self.button_toggled)
        self.radioButtonNine.pressed.connect(self.button_toggled)
        self.radioButtonTwelve.pressed.connect(self.button_toggled)
        
        radioLayout = QHBoxLayout()
        radioLayout.addWidget(self.radioButtonThree)
        radioLayout.addWidget(self.radioButtonSix)
        radioLayout.addWidget(self.radioButtonNine)
        radioLayout.addWidget(self.radioButtonTwelve)
        
        visLayout = QHBoxLayout()
        visLayout.addWidget(self.graphWidget)
        visLayout.addWidget(self.combobox)
        visLayout.addLayout(radioLayout)
        
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
    
    def open_video(self, previous_screen_event: str):
        if previous_screen_event == 'Yes':
            format = '/cubemos'
            
        elif previous_screen_event == 'No':
            format = '/cubemos_converter'
        
        desired_dir = f'{self.BASE_DIR}{format}'
        video_path = self.remove_videos(desired_dir)
        
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(video_path)))
        self.playButton.setEnabled(True)
    
    def remove_videos(self, desired_dir: str):
        desired_path = []
        
        for i in os.listdir(desired_dir):
            if i.endswith('.avi'):
                desired_path.append(i)
        
        #pop the last one and remove it
        if len(desired_path) == 1:
            self.video_path = desired_path[0]
            
        else:
            self.video_path = desired_path.pop()
            for i in range(0, len(desired_path)):
                os.remove(f'{desired_dir}/{desired_path[i]}')
        
        return self.video_path
    
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
        
        frame_position = self.get_frame_position(position)
        
        if self.line == 0:
            self.line = self.graphWidget.addLine(x = 0, pen = pg.mkPen('g', width = 2), movable = False)
            
        else:
            self.graphWidget.removeItem(self.line) 
            self.line = add_line(self.graphWidget, frame_position)
    
    def get_frame_position(self, position):
        duration = self.mediaPlayer.duration()
        if duration == 0:
            frame_position = 0
        else:
            frame_position = position / (duration/self.frames)
        
        return frame_position
    
    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)
        
    def get_current_text_and_plot(self):
        if self.index_analysis == 0:
            if self.welcome_screen_event == 'Yes':
                flag = 'cubemos'
                print('from cubemos')
                self.index_analysis = 1
                
            elif self.welcome_screen_event == 'No':
                flag = 'cubemos_converter'
                print('from cubemos_converter')
                self.index_analysis = 1
            
            os.chdir(f'{self.BASE_DIR}/datatypes')
            subprocess.call(f'python processing.py --flag {flag}', shell = True)
        else:
            pass
        
        plot_cases(self.BASE_DIR, self.graphWidget, self.combobox)
    
    def button_toggled(self):
        frames_pos = radiobutton_toggled(
                            self.BASE_DIR, 
                            self.radioButtonThree, 
                            self.radioButtonSix, 
                            self.radioButtonNine, 
                            self.combobox,
                        )
        
        self.frames = self.initial_frames - frames_pos

class TextFileScreen(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
            
        self.setMinimumHeight(900)
        self.setMinimumWidth(1700)
        self.setWindowTitle('Text Analysis')
        self.setStyleSheet('background-color: rgba(171, 198, 228, 0.5);')
        
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
        self.combobox.addItem('Knees Magnitude')
        self.combobox.addItem('Ankles Magnitude')
        self.combobox.currentTextChanged.connect(self.get_current_text_and_plot)
        
        self.radioButtonThree = QRadioButton('3')
        self.radioButtonSix = QRadioButton('6')
        self.radioButtonNine = QRadioButton('9')
        self.radioButtonTwelve = QRadioButton('12')
        self.radioButtonSix.setChecked(True)
        self.radioButtonThree.pressed.connect(self.button_toggled)
        self.radioButtonSix.pressed.connect(self.button_toggled)
        self.radioButtonNine.pressed.connect(self.button_toggled)
        self.radioButtonTwelve.pressed.connect(self.button_toggled)
        
        radioLayout = QHBoxLayout()
        radioLayout.addWidget(self.radioButtonThree)
        radioLayout.addWidget(self.radioButtonSix)
        radioLayout.addWidget(self.radioButtonNine)
        radioLayout.addWidget(self.radioButtonTwelve)
        
        visLayout = QHBoxLayout()
        visLayout.addWidget(self.graphWidget)
        visLayout.addWidget(self.combobox)
        visLayout.addLayout(radioLayout)
        
        centralwidget.setLayout(visLayout)
    
    def get_current_text_and_plot(self):
        plot_cases(self.BASE_DIR, self.graphWidget, self.combobox)
    
    def button_toggled(self):
        radiobutton_toggled(
                            self.BASE_DIR, 
                            self.radioButtonThree, 
                            self.radioButtonSix, 
                            self.radioButtonNine, 
                            self.combobox,
                        )
