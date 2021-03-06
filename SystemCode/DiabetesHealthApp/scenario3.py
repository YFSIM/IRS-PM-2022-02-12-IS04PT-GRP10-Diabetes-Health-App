import kivy   
from kivy.app import App   
kivy.require('2.0.0')
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button  import Button
from kivy.uix.dropdown  import DropDown
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
#from scenario1 import Diabetes_Health_APPApp1
#from scenario2 import Diabetes_Health_APPApp2
#from main import Diabetes_Health_APPApp

scenario1='Lifestyle Recommender'
scenario2='Predicting Risk of Diabetes'
scenario3='Detect Diabetic Retinopathy'

import requests
import json

Builder.load_file('scenario3.kv')

class scenario3_Layout(Widget):
    def spinner_clicked(self, value):
        print('clicked: '+value)
        
    def button_clicked(self, value):    
        from subprocess import Popen, PIPE
        print('chosen='+value)
        if value == scenario1:
            print('At: '+scenario1+': now')
            #process = Popen(['python3', 'scenario1.py'], stdout=PIPE, stderr=PIPE)
            process = Popen(['scenario1.py'], stdout=PIPE, stderr=PIPE)
        elif value == scenario2:
            print('At: '+scenario2+': now')
            #process = Popen(['python3', 'scenario2.py'], stdout=PIPE, stderr=PIPE)
            process = Popen(['scenario2.py'], stdout=PIPE, stderr=PIPE)
        elif value == scenario3:
            print('At: '+scenario3+': now')
            #process = Popen(['python3', 'scenario3.py'], stdout=PIPE, stderr=PIPE)
            process = Popen(['scenario3.py'], stdout=PIPE, stderr=PIPE)
        else:
            print('At: HOMEPAGE now')
            #process = Popen(['python3', 'main.py'], stdout=PIPE, stderr=PIPE)
            #process = Popen([ 'main.py'], stdout=PIPE, stderr=PIPE)
            #Diabetes_Health_APPApp.run()
        
    def switch_clicked(self, switchObject, switchValue): 
        print(switchValue)
        #self.welcome_label.text = 'FEMALE'
        # if switchValue:
            # print('switchValue='+switchValue)
            # self.ids.click_label.text = f'Switch is ON'
            # #self.scenario1_age_switch.text = 'FEMALE'
        # else:
            # print('switchValue='+switchValue)
            # self.ids.click_label.text = f'Switch is OFF'
            # #self.scenario1_age_switch.text = 'MALE'
    
    def process(self):
        #text = self.root.ids.input.text
        print(text)
    
    def image_selected(self, filename):
        try:
            self.ids.DR_image.source = filename[0]
            print('selected: '+filename)
        except:
            pass
        
        with open('data/scenario3_DiabeticRetinopathy.txt', 'w') as f:
            json.dump(filename[0], f)
    
    def DR_validation(self):
        from subprocess import Popen, PIPE
        process = Popen(['python3', 'scenario3_result.py'], stdout=PIPE, stderr=PIPE)
    
    
class Diabetes_Health_APPApp3(App):
    def build(self):
        return scenario3_Layout()

# run Say Hello App Calss
if __name__ == "__main__":
    Diabetes_Health_APPApp3().run()