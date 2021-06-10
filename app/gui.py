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
        lbl_welcome.setText('<big><b>Welcome to Skeleton Tracking App!</b></big>')
        lbl_welcome.setAlignment(Qt.AlignCenter)
        boxlayout.addWidget(lbl_welcome)
        
        lbl_instructions = QLabel(centralWidget)
        lbl_instructions.setText(
                        '<ol>1. Connect your Intel RealSense camera before start recording!</ol>' + 
                        '<ol>2. Camera should be fixed.</ol>' +
                        '<ol>3. Press start recording and choose your next action.</ol>' +
                        '<ol>4. Press Esc button to stop recording.</ol>'
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
        msg_lic.setText('You do not have the permission to convert your file.')
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
                BASE_DIR = _get_base_dir()
                os.chdir(BASE_DIR + '/cubemos')
                retcode = subprocess.call('python realsense.py', shell = True)
                
                if retcode == 0:
                    print('Go to screen for analysis after recording')
                    self.switch_to_hammer_screen('Yes').show()
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
                
                BASE_DIR = _get_base_dir()
                os.chdir(BASE_DIR + '/cubemos_converter')
                retcode = subprocess.call('python convert_bagfile_skel.py --file ' + fileName, shell = True)
                
                if retcode == 0:
                    print('Go to converter screen')
                    self.switch_to_hammer_screen('No').show()
                else:
                    raise ValueError
            
            except ValueError:
                msg_lic.exec()
            
            except FileNotFoundError:
                msg_format.exec()
            
            except OSError:
                msg_path.exec()
            
            except NotImplementedError:
                pass
                
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
                
                BASE_DIR = _get_base_dir()
                os.chdir(BASE_DIR + '/datatypes')
                retcode = subprocess.call('python hammer_example.py --file ' + fileName, shell = True)
                
                if retcode == 0:
                    print('Text Analysis')
                    self.switch_to_text_screen().show()
            
            except FileNotFoundError:
                msg_format.exec()
            
            except OSError:
                msg_path.exec()
            
            except NotImplementedError:
                pass
            
        elif user_reply == 'Choose you next movement...':
            pass
    
    def switch_to_hammer_screen(self, event:str):
        self.hammer = HammerThrowScreen(event)
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

class HammerThrowScreen(QMainWindow):
    def __init__(self, welcome_screen_event):
        QMainWindow.__init__(self)
        
        self.welcome_screen_event = welcome_screen_event
        
        self.setMinimumHeight(900)
        self.setMinimumWidth(1700)
        self.setWindowTitle('Hammer Throw')
        self.setStyleSheet('background-color: rgba(171, 198, 228, 0.5);')
        
        try:
            self.BASE_DIR = _get_base_dir()
        except OSError:
            raise NotImplementedError
        
        self.index_analysis = 0
        
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
        self.combobox.addItem('Knees Magnitude')
        self.combobox.addItem('Ankles Magnitude')
        self.combobox.currentTextChanged.connect(self.get_current_text_and_plot)
        
        self.radioButtonThree = QRadioButton('3')
        self.radioButtonSix = QRadioButton('6')
        self.radioButtonNine = QRadioButton('9')
        self.radioButtonTwelve = QRadioButton('12')
        self.radioButtonThree.setChecked(True)
        
        self.radioButtonThree = QRadioButton('3')
        self.radioButtonSix = QRadioButton('6')
        self.radioButtonNine = QRadioButton('9')
        self.radioButtonTwelve = QRadioButton('12')
        self.radioButtonSix.setChecked(True)
        self.radioButtonThree.toggled.connect(self.button_toggled)
        self.radioButtonSix.toggled.connect(self.button_toggled)
        self.radioButtonNine.toggled.connect(self.button_toggled)
        self.radioButtonTwelve.toggled.connect(self.button_toggled)
        
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
    
    # Methods related to video playback
    def open_video(self, previous_screen_event: str):
        if previous_screen_event == 'Yes':
            format = '/cubemos'
        elif previous_screen_event == 'No':
            format = '/cubemos_converter'
        
        desired_dir = self.BASE_DIR + format
        
        video_path = self.remove_videos(desired_dir)
        
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(video_path)))
        self.playButton.setEnabled(True)
    
    def remove_videos(self, desired_dir: str):
        desired_path = []
        
        for i in os.listdir(desired_dir):
            if i.endswith('.avi'):
                desired_path.append(i)
        
        # pop the last one and remove it
        self.video_path = desired_path.pop()
        
        for i in range(0, len(desired_path)):
            os.remove(desired_dir + '/' + desired_path[i])
        
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

    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)
        
    def get_current_text_and_plot(self):
        if self.index_analysis == 0:
            if self.welcome_screen_event == 'Yes':
                flag = 'cubemos'
                self.index_analysis = 1
            elif self.welcome_screen_event == 'No':
                flag = 'cubemos_converter'
                self.index_analysis = 1
            
            os.chdir(self.BASE_DIR + '/datatypes')
            subprocess.call('python hammer_example.py --flag ' + flag, shell = True)
        else:
            pass
        
        plot_cases(self.BASE_DIR, self.graphWidget, self.combobox)
    
    def button_toggled(self):
        if self.radioButtonThree.isChecked():
            windows_size_changed(self.BASE_DIR, 3)
            self.combobox.setCurrentText('None')
            
        elif self.radioButtonSix.isChecked():
            windows_size_changed(self.BASE_DIR, 6)
            self.combobox.setCurrentText('None')
            
        elif self.radioButtonNine.isChecked():
            windows_size_changed(self.BASE_DIR, 9)
            self.combobox.setCurrentText('None')
            
        else:
            windows_size_changed(self.BASE_DIR, 12)
            self.combobox.setCurrentText('None')

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
        self.radioButtonThree.toggled.connect(self.button_toggled)
        self.radioButtonSix.toggled.connect(self.button_toggled)
        self.radioButtonNine.toggled.connect(self.button_toggled)
        self.radioButtonTwelve.toggled.connect(self.button_toggled)
        
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
        if self.radioButtonThree.isChecked():
            windows_size_changed(self.BASE_DIR, 3)
            self.combobox.setCurrentText('None')
            
        elif self.radioButtonSix.isChecked():
            windows_size_changed(self.BASE_DIR, 6)
            self.combobox.setCurrentText('None')
            
        elif self.radioButtonNine.isChecked():
            windows_size_changed(self.BASE_DIR, 9)
            self.combobox.setCurrentText('None')
            
        else:
            windows_size_changed(self.BASE_DIR, 12)
            self.combobox.setCurrentText('None')


# Helper utility functions (all classes)
def plot_cases(base_dir:str, graphWidget, combobox):
        txt = combobox.currentText()
        
        if txt == 'Distances':
            graphWidget.clear()
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
            graphWidget.setLabel('bottom', 'frames', **styles)
            graphWidget.addLegend()
            graphWidget.setRange(xRange = (0, max(len(an_lines), len(an_lines))), yRange = (0, max(kn_lines)))
            graphWidget.plot(kn_lines, name = 'Knees', pen = pen_kn)
            graphWidget.plot(an_lines, name = 'Ankles', pen = pen_an)
        
        elif txt == 'Knees Magnitude':
            graphWidget.clear()
            knee_dir_R = base_dir + '/datatypes/logging/knee_right_mag.txt'
            
            with open(knee_dir_R, 'r') as knee_R:
                kn_lines_R = knee_R.readlines()
            knee_R.close()
            
            for i in range(0, len(kn_lines_R)):
                kn_lines_R[i] = float(kn_lines_R[i][:-1])
            
            knee_dir_L = base_dir + '/datatypes/logging/knee_left_mag.txt'
            
            with open(knee_dir_L, 'r') as knee_L:
                kn_lines_L = knee_L.readlines()
            knee_L.close()
            
            for i in range(0, len(kn_lines_L)):
                kn_lines_L[i] = float(kn_lines_L[i][:-1])
            
            pen_kn_r = pg.mkPen(color= 'r', width = 4)
            pen_kn_l = pg.mkPen(color= 'b', width = 4)
            styles = {
                    'color': '#000000', 
                    'font-size': '20px',
                    }
            graphWidget.setLabel('left', 'magnitude', **styles)
            graphWidget.setLabel('bottom', 'frames', **styles)
            graphWidget.addLegend()
            graphWidget.plot(kn_lines_R, name = 'Knee right', pen = pen_kn_r)
            graphWidget.plot(kn_lines_L, name = 'Knee left', pen = pen_kn_l)
        
        elif txt == 'Ankles Magnitude':
            graphWidget.clear()
            ankle_dir_R = base_dir + '/datatypes/logging/ankle_right_mag.txt'
            
            with open(ankle_dir_R, 'r') as ankle_R:
                an_lines_R = ankle_R.readlines()
            ankle_R.close()
            
            for i in range(0, len(an_lines_R)):
                an_lines_R[i] = float(an_lines_R[i][:-1])
            
            ankle_dir_L = base_dir + '/datatypes/logging/ankle_left_mag.txt'
            
            with open(ankle_dir_L, 'r') as ankle_L:
                an_lines_L = ankle_L.readlines()
            ankle_L.close()
            
            for i in range(0, len(an_lines_L)):
                an_lines_L[i] = float(an_lines_L[i][:-1])
            
            pen_an_r = pg.mkPen(color= 'r', width = 4)
            pen_an_l = pg.mkPen(color= 'b', width = 4)
            styles = {
                    'color': '#000000', 
                    'font-size': '20px',
                    }
            graphWidget.setLabel('left', 'magnitude', **styles)
            graphWidget.setLabel('bottom', 'frames', **styles)
            graphWidget.addLegend()
            graphWidget.plot(an_lines_R, name = 'Ankle right', pen = pen_an_r)
            graphWidget.plot(an_lines_L, name = 'Ankle left', pen = pen_an_l)
        
        elif txt == 'None':
            graphWidget.clear()

def windows_size_changed(base_dir: str, wsize: int):
    os.chdir(base_dir + '/datatypes')
    retcode = subprocess.call('python hammer_example.py --wsize ' + str(wsize), shell = True)
    
    if retcode == 0:
        print('Windows size changed')
    else:
        raise NotImplementedError