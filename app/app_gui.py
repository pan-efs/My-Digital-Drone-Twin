#!/usr/bin/env python

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.videoplayer import VideoPlayer
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.properties import ObjectProperty 
from functools import partial
from configuration import Configuration
import sys
import os



# Set-up the window
Window.clearcolor = (1, 1, 1, 1)

class myButton(Button):
    def __init__(self):
        super (myButton, self).__init__()
    
    def disable(self, instance, *args):
        instance.disabled = True
    
    def enable(self, instance, *args):
        instance.enabled = True
    
    def recording(self, instance, *args):
        try:
            realsense_viewer = Configuration()._get_dir('realsense_viewer')
            main_path = Configuration()._get_dir('main')
            os.startfile(realsense_viewer)
        except OSError:
            print('Provided directory cannot be found.')
        
        from cubemos import realsense
        os.chdir(main_path + 'cubemos')
        os.system('python realsense.py')
    
    def offline(self):
        mybtn = Button(text = "Offline Analysis", 
                        size_hint = (None, None),
                        width = 200,
                        height = 75,
                        pos_hint = {'center_x': 0.5},
                        background_color = (119/255.0, 167/255.0, 255/255.0, 1))
        
        return mybtn
    
    def online(self):
        mybtn = Button(text = "Start Recording", 
                        size_hint = (None, None),
                        width = 200,
                        height = 75,
                        pos_hint = {'center_x': 0.5},
                        background_color = (119/255.0, 167/255.0, 255/255.0, 1))
        
        mybtn.bind(on_press = partial(self.recording, mybtn))
        
        return mybtn
    
    def play(self):
        mybtn = Button(text = "Load Video", 
                        size_hint = (None, None),
                        width = 200,
                        height = 75,
                        pos_hint = {'center_x': 0.50},
                        background_color = (119/255.0, 167/255.0, 255/255.0, 1))
        
        return mybtn
    
    def skeletal_tracking(self):
        mybtn = Button(text = "Skeletal Tracking", 
                        size_hint = (None, None),
                        width = 200,
                        height = 75,
                        pos_hint = {'center_x': 0.50},
                        background_color = (119/255.0, 167/255.0, 255/255.0, 1))
        
        return mybtn
    
    def skeletal_submit(self):
        mybtn = Button(text = "Convert video", 
                        size_hint = (None, None),
                        width = 200,
                        height = 75,
                        pos_hint = {'center_x': 0.50},
                        background_color = (119/255.0, 167/255.0, 255/255.0, 1))
        
        return mybtn
    
    def video_visualization_submit(self):
        mybtn = Button(text = "Start analysis", 
                        size_hint = (None, None),
                        width = 200,
                        height = 75,
                        pos_hint = {'center_x': 0.50},
                        background_color = (119/255.0, 167/255.0, 255/255.0, 1))
        
        return mybtn
    
    def offline_analysis_submit(self):
        mybtn = Button(text = "Submit", 
                        size_hint = (None, None),
                        width = 200,
                        height = 75,
                        pos_hint = {'center_x': 0.50},
                        background_color = (119/255.0, 167/255.0, 255/255.0, 1))
        
        return mybtn
    
    def settings(self):
        mybtn = Button(text = "Settings", 
                        size_hint = (None, None),
                        width = 200,
                        height = 75,
                        pos_hint = {'center_x': 0.50},
                        background_color = (119/255.0, 167/255.0, 255/255.0, 1))
        
        return mybtn
    
    def settings_submit(self):
        mybtn = Button(text = "Change settings", 
                        size_hint = (None, None),
                        width = 250,
                        height = 50,
                        pos_hint = {'center_x': 0.50},
                        background_color = (119/255.0, 167/255.0, 255/255.0, 1))
        
        return mybtn
    
    def back_button(self):
        mybtn = Button(text = " ", 
                        size_hint = (None, None),
                        width = 125,
                        height = 75,
                        pos_hint = {'center_x': 0.10},
                        background_normal = 'images\\back_arrow.png',
                        background_down = 'images\\back_arrow.png',
                        background_color = (119/255.0, 167/255.0, 255/255.0, 1))
        
        return mybtn
    
    def yes_or_no(self, txt = 'yes_or_no'):
        mybtn = Button(text = txt,
                        size_hint = (None, None),
                        width = 250,
                        height = 50,
                        pos_hint = {'center_x': 0.50},
                        background_color = (119/255.0, 167/255.0, 255/255.0, 1))
        
        return mybtn

class myLabel(Label):
    def __init__(self):
        super (myLabel, self).__init__()
    
    def intro(self):
        return Label(text = "[color=ff0066][b]Welcome to My Digital Drone Twin![/b][/color]", markup = True)
    
    def skeletal_label(self):
        return Label(text = "[color=0080ff][b]Copy the local path of your desired video.\nFile must be .bag.[/b][/color]", 
                    markup = True,
                    font_size = 20)
    
    def offline_analysis_label(self):
        return Label(text = "[color=0080ff][b]Copy the local path of your desired text file.\nFile must be .txt.[/b][/color]", 
                    markup = True, 
                    font_size = 20)
    
    def settings_label(self):
        return Label(text = "[color=0080ff][b]Provide all directories and then press the button.\nOtherwise an error will be raised later. [/b][/color]", 
                    markup = True, 
                    font_size = 20)
    
    def settings_security_label(self):
        return Label(text = "[color=0080ff][b]Are you sure that you want to continue?\nIf you press YES, the settings will be lost and you should provide them again.\nPress NO to return to main screen.[/b][/color]", 
                    markup = True, 
                    font_size = 20)

class myImage(Image):
    def __init__(self):
        super (myImage, self).__init__()
    
    def logo(self):
        return Image(source = 'images\\kth_logo.png')
    
    def plot_cycling(self):
        return Image(source = 'images\\rpm_info.png')

class myVideo(VideoPlayer):
    def __init__(self):
        super (myVideo, self).__init__()
    
    def play_video(self):
        offline_video = Configuration()._get_dir('offline_analysis')
        return VideoPlayer(source = offline_video,
                    state = 'play', 
                    options={'eos': 'loop'})
    
    def play_mp4(self):
        main_path = Configuration()._get_dir('main')
        return VideoPlayer(source = main_path + 'animations\\videos\\animation.mp4',
                    state = 'play', 
                    options={'eos': 'loop'})
        

class myTextInput(TextInput):
    def __init__(self):
        super (myTextInput, self).__init__()
    
    def text_input(self, wid = 450, hgt = 50, h_text = 'Provide the directory here...'):
        txt = TextInput(hint_text = h_text, 
                        multiline = True,
                        size_hint = (None, None),
                        width = wid,
                        height = hgt,
                        pos_hint = {'center_x': 0.50},
                        background_color = (255/255.0, 255/255.0, 255/255.0, 1))
        
        return txt