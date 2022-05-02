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
#from scenario2 import Diabetes_Health_APPApp2
#from scenario3 import Diabetes_Health_APPApp3
#from main import Diabetes_Health_APPApp

scenario1='Lifestyle Recommender'
scenario2='Predicting Risk of Diabetes'
scenario3='Detect Diabetic Retinopathy'

Builder.load_file('scenario1.kv')

import requests
import json

ip_address = "54.169.12.121"

# defining the api-endpoint
API_ENDPOINT_GET_MOTION = "http://"+ip_address+":5001/getMotionBasedActivities"
API_ENDPOINT_GET_ACTIVITY = "http://"+ip_address+":5001/getActivities"
API_ENDPOINT_GET_RECIPE_MEALTYPE = "http://"+ip_address+":5001/getRecipeBasedOnMeal"
API_ENDPOINT_GET_DIABETIC_RISK = "http://"+ip_address+":5001/diabeticRisk"
API_ENDPOINT_GET_LIFE_IMPROVEMENT = "http://"+ip_address+":5001/lifeStyleImprovement"

# your API key here
API_KEY = "XXXXXXXXXXXXXXXXX"



# data to be sent to api
# data = {'api_dev_key':API_KEY,
#         'api_option':'paste',
#         'api_paste_code':source_code,
#         'api_paste_format':'python'}

class scenario1_Layout(Widget):
    def spinner_clicked(self, value):
        print('clicked: '+value)
        
    def button_clicked(self, value):    
        from subprocess import Popen, PIPE
        print('chosen='+value)
        if value == scenario1:
            print('At: '+scenario1+': now')
            process = Popen(['scenario1.py'], stdout=PIPE, stderr=PIPE)
        elif value == scenario2:
            print('At: '+scenario2+': now')
            process = Popen(['scenario2.py'], stdout=PIPE, stderr=PIPE)
        elif value == scenario3:
            print('At: '+scenario3+': now')
            process = Popen(['scenario3.py'], stdout=PIPE, stderr=PIPE)
        else:
            print('At: HOMEPAGE now')
            #process = Popen(['main.py'], stdout=PIPE, stderr=PIPE)
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
    
    def getDiabeticRisk_button_clicked(self, HighBP, HighChol,Weight,Height,Smoker,Stroke,HeartDiseaseorAttack,PhysActivity,Fruits,Veggies,HvyAlcoholConsump,MentHlth,PhysHlth,DiffWalk,Sex,Age): 
        HighBP = 1 if HighBP else 0
        HighChol = 1 if HighBP else 0
        BMI = int(10000*int(Weight)/int(Height)/int(Height))
        BMI = 1 if HighBP else 0
        Smoker = 1 if HighBP else 0
        Stroke = 1 if HighBP else 0
        HeartDiseaseorAttack = 1 if HighBP else 0
        PhysActivity = 1 if HighBP else 0
        Fruits = 1 if HighBP else 0
        Veggies = 1 if HighBP else 0
        HvyAlcoholConsump = 1 if HighBP else 0
        MentHlth = int(MentHlth)
        PhysHlth = int(PhysHlth)
        MentHlth = 1 if HighBP else 0
        PhysHlth = 1 if HighBP else 0
        DiffWalk = 1 if HighBP else 0
        Sex = 1 if HighBP else 0
        Age = int(Age)
        #sample getDiabeticRisk(1,1,30,1,1,1,1,0,1,0,5,30,0,1,50)
        data = {'HighBP': HighBP, 'HighChol':HighChol,'BMI':BMI, 'Smoker':Smoker,'Stroke':Stroke,'HeartDiseaseorAttack':HeartDiseaseorAttack,'PhysActivity':PhysActivity,'Fruits':Fruits,'Veggies':Veggies,'HvyAlcoholConsump':HvyAlcoholConsump,'MentHlth':MentHlth,'PhysHlth':PhysHlth,'DiffWalk':DiffWalk,'Sex':Sex,'Age':Age}
        try:
            # sending post request and saving response as response object
            r = requests.post(url = API_ENDPOINT_GET_DIABETIC_RISK, json = data)

            # extracting response text
            objresponse = json.loads(r.text)
        except Exception as e:
            print(e)
            return ''
        
        print(objresponse)
        with open('scenario1_DiabeticRisk.txt', 'w') as f:
            json.dump(objresponse, f)
        
        if str(objresponse) == "{'risk': 1}":
            risk_result = 'You are risky in Diabetes!'
        else:
            risk_result = 'You are healthy!'
        #if objresponse[1] == 1:
        self.ids['reducerisk_button_id'].text = risk_result+'\n<Click here to know your risk>'
        #from subprocess import Popen, PIPE
        #print('At: scenario1_result: now')
        #process = Popen(['python3', 'scenario1_result.py'], stdout=PIPE, stderr=PIPE)
    
class Diabetes_Health_APPApp1(App):
    def build(self):
        return scenario1_Layout()

# run Say Hello App Calss
if __name__ == "__main__":
    Diabetes_Health_APPApp1().run()