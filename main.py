from kivy.app import App
# To connect the python file with kivy
from kivy.lang import Builder 
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior

import json
import glob

from pathlib import Path

from datetime import datetime

import random

from hoverable import HoverBehavior

#Load the kivy file
Builder.load_file("design.kv")

class LoginScreen(Screen):
    def login(self,username,password):
        with open("users.json") as file:
            users=json.load(file)
        if username=="":
            self.ids.login_wrong.text="Incorrect username or password!"
        else:
            if username in users and users[username]["password"]==password:
                self.manager.current="login_success_screen"
            else:
                self.ids.login_wrong.text="Incorrect username or password!"
   


       
    def sign_up(self):
        self.manager.current="sign_up_screen"
   

class SignUpScreen(Screen):
    def add_user(self,username,password):
        with open("users.json") as file:
            # It is a dictionary
            users=json.load(file)

            # Each dictionary has a key for sub dictionary and for each sub dictionary, there are three keys 
            users[username]={"username": username, "password": password, "created": datetime.now().strftime("%Y-%m-%d %H-%M-%S")}

            with open("users.json", "w") as file:
                json.dump(users,file)  
            #print(users)

            self.manager.current="sign_up_success_screen"

class SignUpSuccessScreen(Screen):
    def login_page(self):
        self.manager.current="login_screen"

class LoginSuccessScreen(Screen):
    def get_quote(self,feeling):
        feel=feeling.lower()
        available_files=glob.glob("quotes/*txt")

        file_list=[Path(filename).stem for filename in available_files]
        
        if feel in file_list:
            with open("quotes/{}.txt".format(feel)) as file:
                # List of all quotes
                data=file.readlines()
            
            self.ids.quote.text=random.choice(data)
        else:
            self.ids.quote.text="Try another feeling"

    def logout(self):
        self.manager.transition.direction="right"
        self.manager.current="login_screen"


class ImageButton(ButtonBehavior, HoverBehavior, Image):
    pass


class RootWidget(ScreenManager):
    pass

class MainApp(App):
    def build(self):
        return RootWidget()

if __name__=="__main__":
    MainApp().run()
