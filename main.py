import sys
sys.path.append("/".join(x for x in __file__.split("/")[:-1]))
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, NoTransition, CardTransition
#from specialbuttons import ImageButton, LabelButton, ImageButtonSelectable
#from workoutbanner import WorkoutBanner
from functools import partial
from os import walk
#from myfirebase import MyFirebase
from datetime import datetime
#from friendbanner import FriendBanner
import kivy.utils
from kivy.utils import platform
import requests
import json
import traceback
from kivy.graphics import Color, RoundedRectangle
#import helperfunctions

class LoginWindow(Screen):
    pass

class RegistWindow(Screen):
    pass
      
class KasirWindow(Screen):
    pass

class MainApp(App):
    def build(self):
        return Builder.load_file("main.kv")#GUI
    def validate_user(self):
        user= self.root.ids.username_field
        pwd= self.root.ids.pwd_field
        info= self.root.ids.info

        uname=user.text
        passw=pwd.text
    
        if uname== '' or passw=='':
            info.text='[color=#FF0000]username and/ or password required[/color]'
        else:
            if uname=='admin' and passw=='admin':
                self.change_screen("regist_screen")
            else:
                info.text='[color=#FF0000]invalid username and/ or password[/color]'
    
    def change_screen(self, screen_name, direction='forward', mode = ""):
        # Get the screen manager from the kv file
        screen_manager = self.root.ids['screen_manager']
        #print(direction, mode)
        # If going backward, change the transition. Else make it the default
        # Forward/backward between pages made more sense to me than left/right
        if direction == 'forward':
            mode = "push"
            direction = 'left'
        elif direction == 'backwards':
            direction = 'right'
            mode = 'pop'
        elif direction == "None":
            screen_manager.transition = NoTransition()
            screen_manager.current = screen_name
            return

        screen_manager.transition = CardTransition(direction=direction, mode=mode)

        screen_manager.current = screen_name
MainApp().run()