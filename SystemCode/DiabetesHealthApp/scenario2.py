import kivy   
from kivy.app import App   
kivy.require('2.0.0')
from kivy.lang import Builder
from kivy.properties import BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.bubble import Bubble
from kivy.uix.button  import Button
from kivy.uix.dropdown  import DropDown
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
#from scenario1 import Diabetes_Health_APPApp1
#from scenario3 import Diabetes_Health_APPApp3
#from main import Diabetes_Health_APPApp

scenario1='Lifestyle Recommender'
scenario2='Predicting Risk of Diabetes'
scenario3='Detect Diabetic Retinopathy'

activity_table = []
activity_category_table = []
category_table = []
breakfast_table = []
lunch_table = []
dinner_table = []

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

Builder.load_file('scenario2.kv')

class ValidateLabel(Bubble):
    validated = False
    
class FloatInput(FloatLayout):
    bubble_showed = True

    def __init__(self, **kwargs):
        super(FloatInput, self).__init__(**kwargs)
        self.input = scenario2_Layout()
        self.input.bind(text=self.validate)
        self.add_widget(self.input)
        self.bubble = ValidateLabel()
        self.add_widget(self.bubble)

    def validate(self, input, value, min_value=5., max_value=25.):
        self.bubble.ids.label.text = "Number must be between {} and {}".format(min_value, max_value)
        try:
            print(min_value, max_value)
            status = float(min_value) <= float(value) <= float(max_value)
        except Exception as e:
            status = False
            self.bubble.ids.label.text = "Input must be a number"

        if not status:
            if not self.bubble_showed:
                self.input.validated = False
                self.add_widget(self.bubble)
                self.bubble_showed = True
        else:
            print("bubble removed")
            self.input.validated = True
            self.remove_widget(self.bubble)
            self.bubble_showed = False
                
class scenario2_Layout(Widget):   
    validated = BooleanProperty(False)
    def update_spinner_domain_for_category(self, activity_value):
        print('clicked: '+activity_value)
        #self.root.scenario2_activity_spinner.text = activity_value
        category_table = []
        for k in activity_category_table:
            if k[2] == activity_value:
                category_table.append(k[0])
        self.ids.scenario2_category_spinner.values = category_table
        self.ids.scenario2_category_spinner.text = ''

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
    
    def getImprovementSuggestion_button_clicked(self, age,height,weight,activity,motion,noofexerciseaweek,minofexercise,breakfast,lunch,dinner):    
        age = int(age)
        height = int(height)
        weight = int(weight)
        noofexerciseaweek = int(60*float(noofexerciseaweek))
        minofexercise = int(60*float(minofexercise))
        for x in dinner_table:
            if x[1][1] == breakfast:
                breakfast = str(x[0][1])
        for x in lunch_table:
            if x[1][1] == lunch:
                lunch = str(x[0][1])
        for x in dinner_table:
            if x[1][1] == dinner:
                dinner = str(x[0][1])
        #sample getImprovementSuggestion(33,168,76,'bicycling','bicycling, mountain, competitive, racing',3,30,'172791998','5234','58160110')
        data = {'age': age, 'height':height,'weight':weight, 'activity':activity,'motion':motion,'noofexerciseaweek':noofexerciseaweek,'minofexercise':minofexercise,'breakfast':breakfast,'lunch':lunch,'dinner':dinner}
        try:
            # sending post request and saving response as response object
            r = requests.post(url = API_ENDPOINT_GET_LIFE_IMPROVEMENT, json = data)

            # extracting response text
            pastebin_url = r.text
            objresponse = json.loads(pastebin_url)
        except Exception as e:
            print(e)
            return ''
        
        print(objresponse)
        with open('data/scenario2_ImprovementSuggesstion.txt', 'w') as f:
            json.dump(objresponse, f)
            
        from subprocess import Popen, PIPE
        print('At: scenario2_result: now')
        process = Popen(['python3', 'scenario2_result.py'], stdout=PIPE, stderr=PIPE)
    
    def update_padding(self, text_input, *args):
        text_width = text_input._get_text_width(
            text_input.text,
            text_input.tab_width,
            text_input._label_cached
        )
        text_input.padding_x = (text_input.width - text_width)/2
        
class Diabetes_Health_APPApp2(App):
    def build(self):
        return scenario2_Layout()
    
    def on_start(self):
        #self.root.ids['home_button_id'].text='updated from somewhere'
        def update_spinner_domain_for_activity():
            try:
                # sending post request and saving response as response object
                r = requests.post(url = API_ENDPOINT_GET_ACTIVITY)
                # extracting response text
                objresponse = json.loads(r.text)

                #convert json(dict(key, value) to list[[key, value]]
                for i in objresponse:
                    for temp1,temp2 in i.items():
                        activity_table.append(temp2)

                activity_id = self.root.ids['scenario2_activity_spinner']
                activity_id.values = activity_table
            except Exception as e:
                print(e)
                return ''

        update_spinner_domain_for_activity()

        def update_category_basedon_activity():
            for j in activity_table:
                data = {'activity': j}
                try:
                    # sending post request and saving response as response object
                    r = requests.post(url = API_ENDPOINT_GET_MOTION, json = data)
                    # extracting response text
                    objresponse = json.loads(r.text)

                    for i in objresponse:
                        temp = []
                        for temp1,temp2 in i.items():
                            temp.append(temp2)
                        activity_category_table.append(temp)
                except Exception as e:
                    print(e)
                    return ''

        update_category_basedon_activity()

        def update_spinner_domain_for_meal(meal_type,meal_table):
            data = {'mealtype': meal_type}
            try:
                # sending post request and saving response as response object
                r = requests.post(url = API_ENDPOINT_GET_RECIPE_MEALTYPE, json = data)
                # extracting response text
                objresponse = json.loads(r.text)

                #convert json(dict(key, value) to list[[key, value]]
                for i in objresponse:
                    temp = []
                    for temp1,temp2 in i.items():
                        temp.append([temp1,temp2])
                    meal_table.append(temp)

                list_of_meal_description = [x[1][1] for x in meal_table] #meal_table[1][1]=meal_description

                meal_type_id = self.root.ids['scenario2_'+meal_type+'_spinner']
                meal_type_id.values = list_of_meal_description

            except Exception as e:
                print(e)
                return ''

        update_spinner_domain_for_meal('breakfast',breakfast_table)
        update_spinner_domain_for_meal('lunch',lunch_table)
        update_spinner_domain_for_meal('dinner',dinner_table)

# run Say Hello App Calss
if __name__ == "__main__":
    Diabetes_Health_APPApp2().run()