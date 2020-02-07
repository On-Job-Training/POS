from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.config import Config
from kivy.uix.popup import Popup
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.scrollview import ScrollView 
  
# Property that represents a string value 
from kivy.properties import StringProperty 
  
# Static main function that starts the application loop. 
from kivy.base import runTouchApp 
  
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '600')

class setNamePopup(Popup):
    pass

class HomeWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def setName(self,*args):
        setNamePopup().open()
    def home(self,*args):
        HomeWindow().open()

class HomeApp(App):
    def build(self):
        return HomeWindow()
    
if __name__== "__main__":
    oa = HomeApp()
    oa.run()


