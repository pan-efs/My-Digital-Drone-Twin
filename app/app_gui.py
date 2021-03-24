from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.image import Image
from functools import partial

# Set-up the window
Window.clearcolor = (1,1,1,1)
#Window.size = (1280, 720)

class myButton(Button):
    def __init__(self):
        return
    
    def disable(self, instance, *args):
        instance.disabled = True

    def update_offline(self, instance, *args):
        instance.text = "Analysis has started..."
    
    def update_online(self, instance, *args):
        instance.text = "Recording..."
    
    def convertor(self, instance, *args):
        from cubemos_converter import convert_bagfile_skel
    
    def recording(self, instance, *args):
        from cubemos import realsense 
    
    def offline(self):
        mybtn = Button(text = "Offline Analysis", 
                        size_hint = (None, None),
                        width = 200,
                        height = 75,
                        pos_hint = {'center_x': 0.25},
                        background_color = (119/255.0, 167/255.0, 255/255.0, 1))
        
        mybtn.bind(on_press = partial(self.disable, mybtn))
        mybtn.bind(on_press = partial(self.update_offline, mybtn))
        mybtn.bind(on_press = partial(self.convertor, mybtn))
        
        return mybtn
    
    def online(self):
        mybtn = Button(text = "Start Recording", 
                        size_hint = (None, None),
                        width = 200,
                        height = 75,
                        pos_hint = {'center_x': 0.75},
                        background_color = (119/255.0, 167/255.0, 255/255.0, 1))
        
        mybtn.bind(on_press = partial(self.disable, mybtn))
        mybtn.bind(on_press = partial(self.update_online, mybtn))
        mybtn.bind(on_press = partial(self.recording, mybtn))
        
        return mybtn

class myLabel(Label):
    def __init__(self):
        return
    
    def intro(self):
        return Label(text = "[color=ff0066][b]Welcome to My Digital Drone Twin![/b][/color]", markup = True)

class myImage(Image):
    def __init__(self):
        return
    
    def logo(self):
        return Image(source = 'kth_logo.png')

class myDigitalDroneTwin(App):
    def disable_buttons(self, instance, *args):
        instance.disabled = True
    
    def build(self):
        b = myButton()
        on_btn = b.online()
        off_btn = b.offline()
        
        i = myImage()
        img = i.logo()
        
        boxlayout = BoxLayout(spacing = 10, padding = 50)
        boxlayout.add_widget(on_btn)
        boxlayout.add_widget(img)
        boxlayout.add_widget(off_btn)
        
        on_btn.bind(on_press = partial(self.disable_buttons, off_btn))
        off_btn.bind(on_press = partial(self.disable_buttons, on_btn))
        
        return boxlayout


# Run the app
myDigitalDroneTwin().run()