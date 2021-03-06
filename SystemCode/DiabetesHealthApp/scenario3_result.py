import kivy   
from kivy.app import App   
kivy.require('2.1.0') 
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

scenario1='Lifestyle Recommender'
scenario2='Predicting Risk of Diabetes'
scenario3='Detect Diabetic Retinopathy'

import requests
import json

ip_address = "54.169.12.121"

# defining the api-endpoint
API_ENDPOINT_GET_MOTION = "http://"+ip_address+":5001/getMotionBasedActivities"
API_ENDPOINT_GET_ACTIVITY = "http://"+ip_address+":5001/getActivities"
API_ENDPOINT_GET_RECIPE_MEALTYPE = "http://"+ip_address+":5001/getRecipeBasedOnMeal"
API_ENDPOINT_GET_DIABETIC_RISK = "http://"+ip_address+":5001/diabeticRisk"
API_ENDPOINT_GET_LIFE_IMPROVEMENT = "http://"+ip_address+":5001/lifeStyleImprovement"

API_ENDPOINT_GET_RETINAPATHY_LEVEL = "http://"+ip_address+":5001/drDetection"

# your API key here
API_KEY = "XXXXXXXXXXXXXXXXX"

import base64
from PIL import Image
from io import BytesIO
from pathlib import Path
import os

Builder.load_file('scenario3_result.kv')

class scenario3_result_Layout(Widget):
    def spinner_clicked(self, value):
        self.ids.click_label.text = f'You has selected: {value}'
        
    def button_clicked(self, value):    
        from subprocess import Popen, PIPE
        print('chosen='+value)
        if value == scenario1:
            print('At: '+scenario1+': now')
            process = Popen(['python3', 'scenario1.py'], stdout=PIPE, stderr=PIPE)
        elif value == scenario2:
            print('At: '+scenario2+': now')
            process = Popen(['python3', 'scenario2.py'], stdout=PIPE, stderr=PIPE)
        elif value == scenario3:
            print('At: '+scenario3+': now')
            process = Popen(['python3', 'scenario3.py'], stdout=PIPE, stderr=PIPE)
        else:
            print('At: HOMEPAGE now')
            process = Popen(['python3', 'main.py'], stdout=PIPE, stderr=PIPE)
        
    
class Diabetes_Health_APPApp(App):
    def build(self):
        return scenario3_result_Layout()
    
    def on_start(self):
        #self.root.ids['home_button_id'].text='updated from somewhere'
        with open('data/scenario3_DiabeticRetinopathy.txt', 'r') as i:
            image_path = str(i.readlines())[3:-3]  
            print(image_path[len(str(os.getcwd()))+1:])            
            scenario3_DR_image = self.root.ids['DR_image']
            scenario3_DR_image.source = image_path
        

        img =Image.open(image_path)
        im_file = BytesIO()
        img.save(im_file, format="JPEG")
        image_bytes = im_file.getvalue()
        image_b64 = base64.b64encode(image_bytes).decode("utf-8")
        
        data = {'image': str(image_b64)}
        
        try:
            # sending post request and saving response as response object
            r = requests.post(url = API_ENDPOINT_GET_RETINAPATHY_LEVEL, json = data)
            # extracting response text
            objresponse = r.text
        except Exception as e:
            print(e)
            return ''
        
        print(objresponse)
        if objresponse == '{"risk": 4}':
            DRresult = 'Proliferative DR is detected'
        elif objresponse == '{"risk": 3}':
            DRresult = 'Severe DR is detected'
        elif objresponse == '{"risk": 2}':
            DRresult = 'Moderate DR is detected'
        elif objresponse == '{"risk": 1}':
            DRresult = 'Mild DR is detected'
        else:
            DRresult = 'No DR is detected'
            
        self.root.ids['scenario3_result_value'].text = str(DRresult)

if __name__ == "__main__":
    Diabetes_Health_APPApp().run()