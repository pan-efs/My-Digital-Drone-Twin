from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget

import pyqtgraph as pg
import sys, os, subprocess, pickle

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
                
                os.chdir(f'{self.BASE_DIR}/cubemos_converter')
                retcode = subprocess.call(f'python convert_bagfile_skel.py --file {fileName}', shell = True)
                
                if retcode == 0:
                    print('Go to converter screen')
                    self.switch_to_hammer_screen('No').show()
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
        self.frames = graph_length(self.BASE_DIR, self.welcome_screen_event)
        
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
        radiobutton_toggled(
                            self.BASE_DIR, 
                            self.radioButtonThree, 
                            self.radioButtonSix, 
                            self.radioButtonNine, 
                            self.combobox
                        )

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
                            self.combobox
                        )


# Helper functions
def _get_base_dir():
    frozen = 'not'
    if getattr(sys, 'frozen', False):
        frozen = 'ever so'
        BASE_DIR = sys._MEIPASS
    else:
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    return BASE_DIR

def add_line(graphWidget, position):
    new_line = graphWidget.addLine(
                                x = position, 
                                pen = pg.mkPen(color= 'g', width = 2), 
                                angle = 90, 
                                movable = False
                            )
    return new_line

def graph_length(base_dir:str, screen: str):
    if screen == 'Yes':
        folder = 'cubemos'
        txt = 'get_3d_joints.txt'
    else:
        folder = 'cubemos_converter'
        txt = 'write_3d_joints_from_video.txt'
    
    _dir = f'{base_dir}/{folder}/logging/{txt}'
    graph = open(_dir, 'r').readlines()
    
    graph_len = len(graph)/18
    
    print(graph_len)
    
    return graph_len

def radiobutton_toggled(base_dir: str, radiobutton1, radiobutton2, radiobutton3, combobox):
    if radiobutton1.isDown():
        windows_size_changed(base_dir, 3)
        combobox.setCurrentText('None')
            
    elif radiobutton2.isDown():
        windows_size_changed(base_dir, 6)
        combobox.setCurrentText('None')
            
    elif radiobutton3.isDown():
        windows_size_changed(base_dir, 9)
        combobox.setCurrentText('None')
            
    else:
        windows_size_changed(base_dir, 12)
        combobox.setCurrentText('None')

def plot_cases(base_dir:str, graphWidget, combobox):
        txt = combobox.currentText()
        
        if txt == 'Distances':
            graphWidget.clear()
            
            knees_dir = f'{base_dir}/datatypes/logging/knee_distances.txt'
            with open(knees_dir, 'rb') as knees:
                kn_lines = pickle.load(knees)
            
            ankles_dir = f'{base_dir}/datatypes/logging/ankle_distances.txt'
            with open(ankles_dir, 'rb') as ankles:
                an_lines = pickle.load(ankles)
            
            pen_kn = pg.mkPen(color= 'r', width = 4)
            pen_an = pg.mkPen(color= 'b', width = 4)
            styles = {
                    'color': '#000000', 
                    'font-size': '20px',
                    }
            graphWidget.setLabel('left', 'meters', **styles)
            graphWidget.setLabel('bottom', 'frames', **styles)
            graphWidget.addLegend()
            graphWidget.setRange(xRange = (0, max(len(an_lines), len(an_lines))), yRange = (0, max(max(kn_lines), max(an_lines))))
            graphWidget.plot(kn_lines, name = 'Knees', pen = pen_kn)
            graphWidget.plot(an_lines, name = 'Ankles', pen = pen_an)
            
        
        elif txt == 'Knees Magnitude':
            graphWidget.clear()
            
            knee_dir_R = f'{base_dir}/datatypes/logging/knee_right_mag.txt'
            with open(knee_dir_R, 'rb') as knee_R:
                kn_lines_R = pickle.load(knee_R)
            
            knee_dir_L = f'{base_dir}/datatypes/logging/knee_left_mag.txt'
            with open(knee_dir_L, 'rb') as knee_L:
                kn_lines_L = pickle.load(knee_L)
            
            pen_kn_r = pg.mkPen(color= 'r', width = 4)
            pen_kn_l = pg.mkPen(color= 'b', width = 4)
            styles = {
                    'color': '#000000', 
                    'font-size': '20px',
                    }
            graphWidget.setLabel('left', 'magnitude', **styles)
            graphWidget.setLabel('bottom', 'frames', **styles)
            graphWidget.addLegend()
            graphWidget.setRange(xRange = (0, len(kn_lines_R)), yRange = (0, max(max(kn_lines_R), max(kn_lines_L))))
            graphWidget.plot(kn_lines_R, name = 'Knee right', pen = pen_kn_r)
            graphWidget.plot(kn_lines_L, name = 'Knee left', pen = pen_kn_l)
        
        elif txt == 'Ankles Magnitude':
            graphWidget.clear()
            
            ankle_dir_R = f'{base_dir}/datatypes/logging/ankle_right_mag.txt'
            with open(ankle_dir_R, 'rb') as ankle_R:
                an_lines_R = pickle.load(ankle_R)
            
            ankle_dir_L = f'{base_dir}/datatypes/logging/ankle_left_mag.txt'
            with open(ankle_dir_L, 'rb') as ankle_L:
                an_lines_L = pickle.load(ankle_L)
            
            pen_an_r = pg.mkPen(color= 'r', width = 4)
            pen_an_l = pg.mkPen(color= 'b', width = 4)
            styles = {
                    'color': '#000000', 
                    'font-size': '20px',
                    }
            graphWidget.setLabel('left', 'magnitude', **styles)
            graphWidget.setLabel('bottom', 'frames', **styles)
            graphWidget.addLegend()
            graphWidget.setRange(xRange = (0, len(an_lines_R)), yRange = (0, max(max(an_lines_R), max(an_lines_L))))
            graphWidget.plot(an_lines_R, name = 'Ankle right', pen = pen_an_r)
            graphWidget.plot(an_lines_L, name = 'Ankle left', pen = pen_an_l)
        
        elif txt == 'None':
            graphWidget.clear()

def windows_size_changed(base_dir: str, wsize: int):
    os.chdir(f'{base_dir}/datatypes')
    retcode = subprocess.call(f'python processing.py --wsize {wsize}', shell = True)
    
    if retcode == 0:
        print('Windows size changed to', wsize)
    else:
        raise NotImplementedError
    