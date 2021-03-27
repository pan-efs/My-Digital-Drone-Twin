#!/usr/bin/env python

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.properties import ObjectProperty 
from functools import partial
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
            os.startfile('C:\\Users\\Public\\Desktop\\Intel RealSense Viewer.lnk')
        except OSError:
            print('Provided directory cannot be found.')
        
        from cubemos import realsense
        os.chdir('C:\\Users\\Drone\\Desktop\\Panagiotis\\My-Digital-Drone-Twin\\cubemos')
        os.system('python realsense.py')
    
    def converted_video(self, instance, *args):
        os.startfile('C:\\Users\\Drone\\Desktop\\Panagiotis\\Moving camera\\standstill-panagiotis.avi')
    
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
        
        #mybtn.bind(on_press = partial(self.converted_video, mybtn))
        
        return mybtn
    
    def skeletal_tracking(self):
        mybtn = Button(text = "Skeletal Tracking", 
                        size_hint = (None, None),
                        width = 200,
                        height = 75,
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

class myImage(Image):
    def __init__(self):
        super (myImage, self).__init__()
    
    def logo(self):
        return Image(source = 'images\\kth_logo.png')

class myTextInput(TextInput):
    def __init__(self):
        super (myTextInput, self).__init__()
    
    def text_input(self):
        txt = TextInput(hint_text = "Provide the directory here...", 
                        multiline = False,
                        size_hint = (None, None),
                        width = 450,
                        height = 50,
                        pos_hint = {'center_x': 0.50},
                        background_color = (255/255.0, 255/255.0, 255/255.0, 1))
        
        return txt

class screenOne(Screen):
    def __init__(self, **kwargs):
        super (screenOne, self).__init__(**kwargs)
        
        b = myButton()
        on_btn = b.online()
        off_btn = b.offline()
        play_btn = b.play()
        skel_btn = b.skeletal_tracking()
        
        i = myImage()
        img = i.logo()
        
        boxlayout = BoxLayout(orientation = 'vertical', 
                            spacing = 25, 
                            padding = 60)
        
        boxlayout.add_widget(img)
        boxlayout.add_widget(on_btn)
        boxlayout.add_widget(skel_btn)
        boxlayout.add_widget(off_btn)
        boxlayout.add_widget(play_btn)
        
        off_btn.bind(on_press = self.change_to_offline_analysis)
        play_btn.bind(on_press = self.change_to_filechooser)
        skel_btn.bind(on_press = self.change_to_skeletal)
        
        self.add_widget(boxlayout)
    
    def change_to_skeletal(self, *args):
        self.manager.current = 'skeletal'
    
    def change_to_offline_analysis(self, *args):
        self.manager.current = 'offline_analysis'
    
    def change_to_filechooser(self, *args):
        self.manager.current = 'filechooser'

class skeletal_screen(Screen):
    def __init__(self, **kwargs):
        super (skeletal_screen, self).__init__(**kwargs)
        
        self.t = myTextInput()
        self.txt = self.t.text_input()
        
        b = myButton()
        back_arrow = b.back_button()
        
        l = myLabel()
        skel_lbl = l.skeletal_label()
        
        i = myImage()
        kth_logo = i.logo()
        
        boxlayout = BoxLayout(orientation = 'vertical', spacing = 40, padding = 60)
        boxlayout.add_widget(kth_logo)
        boxlayout.add_widget(skel_lbl)
        boxlayout.add_widget(self.txt)
        boxlayout.add_widget(self.skeletal_submit())
        boxlayout.add_widget(back_arrow)
        
        back_arrow.bind(on_press = self.change_to_main)
        
        self.add_widget(boxlayout)
    
    def save_path(self, path: str):
        open('converter_path.txt', 'w').close()
        file = open('converter_path.txt', 'a')
        file.write(path)
        file.close()
        print("GOT PATH:" + path)
    
    def skeletal_submit(self):
        mybtn = Button(text = "Submit", 
                        size_hint = (None, None),
                        width = 200,
                        height = 75,
                        pos_hint = {'center_x': 0.50},
                        background_color = (119/255.0, 167/255.0, 255/255.0, 1))
        
        mybtn.bind(on_press = lambda *a: self.save_path(self.txt.text))
        mybtn.bind(on_press = self.converter)
        
        return mybtn
    
    def change_to_main(self, *args):
        self.manager.current = 'screen1'
    
    def converter(self, instance, *args):
        from cubemos_converter import convert_bagfile_skel
        os.chdir('C:\\Users\\Drone\\Desktop\\Panagiotis\\My-Digital-Drone-Twin\\cubemos_converter')
        os.system('python convert_bagfile_skel.py')

class offline_analysis_screen(Screen):
    def __init__(self, **kwargs):
        super (offline_analysis_screen, self).__init__(**kwargs)
        
        b = myButton()
        back_arrow = b.back_button()
        
        t = myTextInput()
        txt = t.text_input()
        
        l = myLabel()
        offline_lbl = l.offline_analysis_label()
        
        i = myImage()
        kth_logo = i.logo()
        
        boxlayout = BoxLayout(orientation = 'vertical', spacing = 20, padding = 50)
        boxlayout.add_widget(kth_logo)
        boxlayout.add_widget(offline_lbl)
        boxlayout.add_widget(txt)
        boxlayout.add_widget(self.offline_analysis_submit())
        boxlayout.add_widget(back_arrow)
        
        back_arrow.bind(on_press = self.change_to_main)
        
        self.add_widget(boxlayout)
    
    def offline_analysis_submit(self):
        mybtn = Button(text = "Submit", 
                        size_hint = (None, None),
                        width = 200,
                        height = 75,
                        pos_hint = {'center_x': 0.50},
                        background_color = (119/255.0, 167/255.0, 255/255.0, 1))
        
        #mybtn.bind(on_press = lambda *a: self.save_path(self.txt.text))
        mybtn.bind(on_press = self.biomechanics_analysis)
        mybtn.bind(on_press = self.video_analysis)
        
        return mybtn
    
    def change_to_main(self, *args):
        self.manager.current = 'screen1'
    
    def biomechanics_analysis(self, instance, *args):
        os.chdir('C:\\Users\\Drone\\Desktop\\Panagiotis\\My-Digital-Drone-Twin\\samples')
        os.system('python biomechanics3D_example.py')
    
    def video_analysis(self, instance, *args):
        os.startfile('C:\\Users\\Drone\\Desktop\\Panagiotis\\Moving camera\\standstill_martin.avi')

class Filechooser(BoxLayout):
    def select(self, *args):
        try: 
            self.label.text = args[1][0]
        except: 
            pass

class Navigation(Filechooser):
    def __init__(self):
        super (Navigation, self).__init__()
    
    def choose_file(self):
        nav = Filechooser()
        return nav
    
class filechooser_screen(Screen):
    def __init__(self, **kwargs):
        super (filechooser_screen, self).__init__(**kwargs)
        
        b = myButton()
        back_btn = b.back_button()
        
        n = Navigation()
        files = n.choose_file()
        
        boxlayout = BoxLayout(orientation = 'vertical')
        boxlayout.add_widget(files)
        boxlayout.add_widget(back_btn)
        
        back_btn.bind(on_press = self.change_to_main)
        
        self.add_widget(boxlayout)
    
    def change_to_main(self, *args):
        self.manager.current = 'screen1'

class myDigitalDroneTwin(App):
    
    def build(self):
        screen_manager = ScreenManager()
        screen1 = screenOne(name = 'screen1')
        skeletal = skeletal_screen(name = 'skeletal')
        offline_analysis = offline_analysis_screen(name = 'offline_analysis')
        filechooser = filechooser_screen(name = 'filechooser')
        
        
        screen_manager.add_widget(screen1)
        screen_manager.add_widget(skeletal)
        screen_manager.add_widget(offline_analysis)
        screen_manager.add_widget(filechooser)
        
        return screen_manager


# Run the app
myDigitalDroneTwin().run()