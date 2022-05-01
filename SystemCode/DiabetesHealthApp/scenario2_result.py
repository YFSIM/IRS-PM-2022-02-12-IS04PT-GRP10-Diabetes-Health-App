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

Builder.load_file('scenario2_result.kv')

class scenario2_result_Layout(Widget):
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
        return scenario2_result_Layout()
    
    def on_start(self):
        #self.root.ids['home_button_id'].text='updated from somewhere'
        with open('data/scenario2_ImprovementSuggesstion.txt', 'r') as file:
            data = file.read().replace('\n', '')
            print(data)
            data = data[1:-1]
            data = data.replace(', ', '\n')
            data = data.replace('"', ' ')
            #data = data[:-30] + '\n' + data[-30:]
            scenario3_output_result_id = self.root.ids['scenario2_output_result']
            scenario3_output_result_id.text = data

if __name__ == "__main__":
    Diabetes_Health_APPApp().run()