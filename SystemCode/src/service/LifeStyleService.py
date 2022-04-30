import sys
import os
import pandas as pd

import pickle
import json
from collections import namedtuple
from json import JSONEncoder
import RecipeService
from RecipeService import *
import ActivityService
from ActivityService import *


def dt_lsmodel():
    module_path = os.path.abspath(os.path.join('../..'))
    filepath = module_path +  'model/' + 'decision_tree_classifier.pkl'
    print(filepath)


    decision_tree_model_pkl = open(filepath, 'rb')
    decision_tree_model = pickle.load(decision_tree_model_pkl)
    return decision_tree_model

def knn_lsmodel():
    module_path = os.path.abspath(os.path.join('../..'))
    filepath = module_path + 'model/' + 'knn_classifier.pkl'
    print(filepath)


    knn_model_pkl = open(filepath, 'rb')
    knn_model = pickle.load(knn_model_pkl)
    return knn_model
    
def predictBMI(input,model_type):
    model = dt_lsmodel()
    if model_type == 'knn':
        model = knn_lsmodel()
    predict_value = model.predict(input)
    return predict_value

def test():
    df_predict = pd.read_csv("bmi_test.csv")
    print(predictBMI(df_predict,"knn"))

def customHealthDecoder(healthDict):
    return namedtuple('X', healthDict.keys())(*healthDict.values())

def physicalActivity(currentpa,target,currentMET,minofexercise,currentNoOfExercise,activity):
    physical_activity_advice = ''
    if currentpa < target:

        if (currentNoOfExercise < 5):
            pa_add_5 = 5 * minofexercise * currentMET

            if (pa_add_5 >= target):
                physical_activity_advice = 'Please increase your number of exercise to 5x a week'
            elif (pa_add_5 < target and minofexercise < 30):

                pa_add_5_30 = 5 * 30 * currentMET

                if (pa_add_5_30 < target):
                    paDataList = json.loads(find_motion_activity(activity))

                    for index in range(len(paDataList)):

                        if paDataList[index]['met'] > currentMET:
                            countPA = 5 * 30 * paDataList[index]['met']
                            if (countPA >= target):
                                physical_activity_advice = 'Please increase your number of exercise to 5x a week and each 30 minutes and try to do ' + paDataList[index]['specificmotion'] 
                                break
                    if physical_activity_advice == '':
                        physical_activity_advice = 'Please increase your number of exercise to 5x a week and each 30 minutes and try to do moderate type of exercise'                                
                else:
                    physical_activity_advice = 'Please increase your number of exercise to 5x a week and each 30 minutes'
            elif (pa_add_5 < target and minofexercise > 30):
                paDataList = json.loads(find_motion_activity(activity))
                for index in range(len(paDataList)):
                    if paDataList[index]['met'] > currentMET:
                        countPA = 5 * 30 * paDataList[index]['met']
                        if (countPA >= target):
                            physical_activity_advice = 'Please increase your number of exercise to 5x a week and each 30 minutes and try to do ' + paDataList[index]['specificmotion'] 
                            break
                if physical_activity_advice == '':
                    physical_activity_advice = 'Please increase your number of exercise to 5x a week and each 30 minutes and try to do moderate type of exercise'                                
        elif (minofexercise < 30):  
            pa_add_30 = currentNoOfExercise * 30 * currentMET
            if (pa_add_30 < target):
                paDataList = json.loads(find_motion_activity(activity))
                for index in range(len(paDataList)):
                    if paDataList[index]['met'] > currentMET:
                        countPA = currentNoOfExercise * 30 * paDataList[index]['met']
                        if (countPA >= target):
                            physical_activity_advice = 'Please increase your exercise time to 30 minutes and try to do ' + paDataList[index]['specificmotion'] 
                            break
                if physical_activity_advice == '':
                    physical_activity_advice = 'Please increase your number of exercise to 5x a week and each 30 minutes and try to do moderate type of exercise'                                
            else:
                physical_activity_advice = 'Please increase your exercise time to 30 minutes'
        elif(minofexercise >= 30 and currentNoOfExercise >= 5):
            paDataList = json.loads(find_motion_activity(activity))
            for index in range(len(paDataList)):
                if paDataList[index]['met'] > currentMET:
                    countPA = currentNoOfExercise * 30 * paDataList[index]['met']
                    if (countPA >= target):
                        physical_activity_advice = 'Please increase your exercise time to 30 minutes and try to do ' + paDataList[index]['specificmotion'] 
                        break
            if physical_activity_advice == '':
                physical_activity_advice = 'Please increase your number of exercise to 5x a week and each 30 minutes and try to do moderate type of exercise'              
        else:
            physical_activity_advice = 'Please increase your exercise activity'
    return physical_activity_advice

def predictHealthRisk(request_data):
    
    physical_activity_advice = ''
    b_meal_advice = ''
    l_meal_advice = ''
    d_meal_advice = ''
    try:

        # Parse JSON into an object with attributes corresponding to dict keys.
        healthData = json.loads(request_data, object_hook=customHealthDecoder)
        bmi_actual = healthData.weight / ((healthData.height/100) * (healthData.height/100))

        paData = json.loads(find_met(healthData.activity, healthData.motion), object_hook=customHealthDecoder)
        pa = healthData.noofexerciseaweek * healthData.minofexercise * paData[0].METs

        jsonbreakFast = json.loads(calculate_ingredient(healthData.breakfast))

        df_breakfast = pd.json_normalize(jsonbreakFast)
        df_breakfast['pa'] = pa
        df_breakfast['age_x'] = healthData.age
        df_breakfast['mealtime']=1

        bmi_breakfast= predictBMI(df_breakfast,'knn')[0]

        #------------------------------------------------------------
        jsonLunch = json.loads(calculate_ingredient(healthData.lunch))

        df_lunch = pd.json_normalize(jsonLunch)
        df_lunch['pa'] = pa
        df_lunch['age_x'] = healthData.age
        df_lunch['mealtime']=1

        bmi_lunch= predictBMI(df_lunch,'knn')[0]

        #------------------------------------------------------------
        jsonDinner = json.loads(calculate_ingredient(healthData.dinner))

        df_dinner = pd.json_normalize(jsonDinner)
        df_dinner['pa'] = pa
        df_dinner['age_x'] = healthData.age
        df_dinner['mealtime']=1

        bmi_dinner= predictBMI(df_dinner,'knn')[0]
        
        if (pa < 500 and bmi_actual >= 24.9):
            physical_activity_advice = physicalActivity(pa,500,paData[0].METs,healthData.minofexercise,healthData.noofexerciseaweek,healthData.activity)
        elif (pa < 1000 and pa >= 500 and bmi_actual >= 24.9):
            physical_activity_advice = physicalActivity(pa,500,paData[0].METs,healthData.minofexercise,healthData.noofexerciseaweek,healthData.activity)
        elif (bmi_actual < 24.9):
            physical_activity_advice = 'Please increase your exercise activity for a healthier you'
        else:
            physical_activity_advice = 'Please increase your exercise activity to reduce your health risk'

        
        if (bmi_breakfast >= 24.9):
            b_meal_advice = 'Please get healthier breakfast'
        if (bmi_lunch >= 24.9):
            l_meal_advice = 'Please get healthier lunch'
        if (bmi_dinner >= 24.9):
            d_meal_advice = 'Please get healthier dinner'            
        
        
            
        print(bmi_actual)
        print(bmi_breakfast)
        print(bmi_lunch)
        print(bmi_dinner)
    
    except Exception as e: 
        print(e)        
        print('Ooopss')
    
    response = Response()
    response.breakfastMealAdvice = b_meal_advice
    response.lunchMealAdvice = l_meal_advice
    response.dinnerMealAdvice = d_meal_advice
    response.physicalExerciseAdvice = physical_activity_advice
    
    jsonStr = json.dumps(response.__dict__)
    return jsonStr
    
         

class Response:
    breakfastMealAdvice = ''
    lunchMealAdvice = ''
    dinnerMealAdvice = ''
    physicalExerciseAdvice = ''

     

testdata = '{\
    "age":33,\
    "height": 168,\
    "weight": 76,\
    "activity": "conditioning exercise",\
    "motion": "stretching, mild",\
    "noofexerciseaweek":5,\
    "minofexercise":30,\
    "breakfast":"172791998",\
    "lunch":"5234",\
    "dinner":"58160110"}'
predictHealthRisk(testdata)