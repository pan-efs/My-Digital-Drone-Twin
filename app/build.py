from screens import ScreenOne, SkeletalScreen, OfflineAnalysisScreen, VideosVisualizationScreen, FileChooserScreen, SettingsScreen, SettingsSecurityScreen
from kivy.uix.screenmanager import ScreenManager
from kivy.app import App

class MyDigitalDroneTwin(App):
    
    def build(self):
        
        screen_manager = ScreenManager()
        screen1 = ScreenOne(name = 'screen1')
        skeletal = SkeletalScreen(name = 'skeletal')
        offline_analysis = OfflineAnalysisScreen(name = 'offline_analysis')
        filechooser = FileChooserScreen(name = 'filechooser')
        #video_visualization = VideosVisualizationScreen(name = 'video_visualization')
        settings = SettingsScreen(name = 'settings')
        settings_security = SettingsSecurityScreen(name = 'settings_security')
        
        screen_manager.add_widget(screen1)
        screen_manager.add_widget(skeletal)
        screen_manager.add_widget(offline_analysis)
        screen_manager.add_widget(filechooser)
        #screen_manager.add_widget(video_visualization)
        screen_manager.add_widget(settings)
        #screen_manager.add_widget(settings_security)
        
        return screen_manager
