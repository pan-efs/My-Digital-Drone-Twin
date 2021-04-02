from app_gui import myButton, myLabel, myImage, myVideo, myTextInput
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty 
from functools import partial
from configuration import Configuration
import sys
import os

class ScreenOne(Screen):
    def __init__(self, **kwargs):
        super (ScreenOne, self).__init__(**kwargs)
        
        b = myButton()
        on_btn = b.online()
        off_btn = b.offline()
        play_btn = b.play()
        skel_btn = b.skeletal_tracking()
        settings_btn = b.settings()
        
        i = myImage()
        img = i.logo()
        
        boxlayout = BoxLayout(orientation = 'vertical', 
                            spacing = 20, 
                            padding = 50)
        
        boxlayout.add_widget(img)
        boxlayout.add_widget(on_btn)
        boxlayout.add_widget(skel_btn)
        boxlayout.add_widget(off_btn)
        boxlayout.add_widget(play_btn)
        boxlayout.add_widget(settings_btn)
        
        off_btn.bind(on_press = self.change_to_offline_analysis)
        play_btn.bind(on_press = self.change_to_filechooser)
        skel_btn.bind(on_press = self.change_to_skeletal)
        settings_btn.bind(on_press = self.change_to_settings)
        
        self.add_widget(boxlayout)
    
    def change_to_skeletal(self, *args):
        self.manager.current = 'skeletal'
    
    def change_to_offline_analysis(self, *args):
        self.manager.current = 'offline_analysis'
    
    def change_to_filechooser(self, *args):
        self.manager.current = 'filechooser'
    
    def change_to_settings(self, *args):
        self.manager.current = 'settings'

class SkeletalScreen(Screen):
    def __init__(self, **kwargs):
        super (SkeletalScreen, self).__init__(**kwargs)
        
        self.t = myTextInput()
        self.txt = self.t.text_input()
        
        b = myButton()
        back_arrow = b.back_button()
        skl_submit = b.skeletal_submit()
        
        l = myLabel()
        skel_lbl = l.skeletal_label()
        
        i = myImage()
        kth_logo = i.logo()
        
        boxlayout = BoxLayout(orientation = 'vertical', 
                            spacing = 40, 
                            padding = 60)
        boxlayout.add_widget(kth_logo)
        boxlayout.add_widget(skel_lbl)
        boxlayout.add_widget(self.txt)
        boxlayout.add_widget(skl_submit)
        boxlayout.add_widget(back_arrow)
        
        back_arrow.bind(on_press = self.change_to_main)
        #skl_submit.bind(on_press = self.save_path(self.txt.text))
        skl_submit.bind(on_press = self.converter)
        
        self.add_widget(boxlayout)
    
    def save_path(self, path: str):
        open('converter_path.txt', 'w').close()
        file = open('converter_path.txt', 'a')
        file.write(path)
        file.close()
        print("GOT PATH:" + path)
    
    def change_to_main(self, *args):
        self.manager.current = 'screen1'
    
    def converter(self, instance, *args):
        from cubemos_converter import convert_bagfile_skel
        try:
            main_path = Configuration()._get_dir('main')
            os.chdir(main_path + 'cubemos_converter')
            os.system('python convert_bagfile_skel.py')
        except OSError:
            print('Provided directory cannot be found.')

class OfflineAnalysisScreen(Screen):
    def __init__(self, **kwargs):
        super (OfflineAnalysisScreen, self).__init__(**kwargs)
        
        b = myButton()
        back_arrow = b.back_button()
        offline_analysis_submit = b.offline_analysis_submit()
        
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
        boxlayout.add_widget(offline_analysis_submit)
        boxlayout.add_widget(back_arrow)
        
        back_arrow.bind(on_press = self.change_to_main)
        offline_analysis_submit.bind(on_press = self.change_to_videovisualization)
        
        self.add_widget(boxlayout)
    
    def change_to_main(self, *args):
        self.manager.current = 'screen1'
    
    def change_to_videovisualization(self, *args):
        self.manager.current = 'video_visualization'

class VideosVisualizationScreen(Screen):
    def __init__(self, **kwargs):
        super (VideosVisualizationScreen, self).__init__(**kwargs)
        
        v = myVideo()
        video = v.play_video()
        animation = v.play_mp4()
        
        b = myButton()
        back_btn = b.back_button()
        start_btn = b.video_visualization_submit()
        
        i = myImage()
        kth_logo = i.logo()
        
        boxlayout = BoxLayout(orientation = 'vertical', spacing = 20, padding = 40)
        boxlayout.add_widget(animation)
        boxlayout.add_widget(video)
        boxlayout.add_widget(back_btn)
        #boxlayout.add_widget(start_btn)
        
        back_btn.bind(on_press = self.change_to_offline_analysis)
        start_btn.bind(on_press = self.biomechanics_analysis)
        
        self.add_widget(boxlayout)
    
    def biomechanics_analysis(self, instance, *args):
        try:
            main_path = Configuration()._get_dir('main')
            os.chdir(main_path + 'samples')
            os.system('python biomechanics3D_example.py')
        except OSError:
            print('Provided directory cannot be found.')
    
    def change_to_offline_analysis(self, *args):
        self.manager.current = 'offline_analysis'

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
    
class FileChooserScreen(Screen):
    def __init__(self, **kwargs):
        super (FileChooserScreen, self).__init__(**kwargs)
        
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

class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super (SettingsScreen, self).__init__(**kwargs)
        
        open('settings.txt', 'w').close()
        f = open('settings.txt', 'w')
        f.write('Not provided\nNot provided\nNot provided\n')
        f.close()
        
        b = myButton()
        back_btn = b.back_button()
        settings_submit_btn = b.settings_submit()
        
        t = myTextInput()
        main_btn = t.text_input(wid = 500, hgt = 100, 
                                h_text = 'Main path here...\n' + 'RealSense Viewer here...\n' +
                                        'Offline analysis here...')
        
        l = myLabel()
        settings_lbl = l.settings_label()
        
        boxlayout = BoxLayout(orientation = 'vertical', spacing = 25, padding = 50)
        boxlayout.add_widget(settings_lbl)
        boxlayout.add_widget(main_btn)
        boxlayout.add_widget(settings_submit_btn)
        boxlayout.add_widget(back_btn)
        
        settings_submit_btn.bind(on_press = lambda *a:self.save_path(main_btn.text))

        back_btn.bind(on_press = self.change_to_main)
        
        self.add_widget(boxlayout)
    
    def save_path(self, path: str):
        if path != '':
            try:
                file = open('settings.txt', 'a')
                file.writelines(path + '\n')
                file.close()
                print("GOT PATH:" + path)
            except:
                print('File cannot open.')
        else:
            print('Path was empty! Provide a directory...')
    
    def change_to_main(self, *args):
        self.manager.current = 'screen1'