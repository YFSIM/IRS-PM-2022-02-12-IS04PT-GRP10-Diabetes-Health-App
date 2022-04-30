import sys
import os
import pandas as pd
import json
import numpy as np
from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask import request, jsonify
from pandas import json_normalize
from collections import namedtuple



app = Flask(__name__)
api = Api(app)


module_path = os.path.abspath(os.path.join(''))

sys.path.append(module_path+"src/datamodel")
sys.path.append(module_path+"src/service")


import LifeStyle
from LifeStyleService import predictBMI
from DiabeticRiskService import predictDiabeticRisk
from LifeStyleService import predictHealthRisk
from RecipeService import find_recipe_by_mealtype
from ActivityService import find_activity
from ActivityService import find_motion_activity
from DRDetectionService import getRetinopathyLevel

#import src.datamodel.LifeStyle 

# class LifeStyle(Resource):
#     # methods go here
#     def post(self):
#         print('Test')
#         #print(self)
#         df_predict = pd.read_csv("bmi_test.csv")
#         print(predictBMI(df_predict,'dt'))
#         pass

# api.add_resource(LifeStyle, '/lifeStyle')  # '/users' is our entry point
def customDecoder(objDict):
    return namedtuple('X', objDict.keys())(*objDict.values())

@app.route('/lifeStyle', methods=['POST'])
def lifeStyle():
    print('LifeStyle call')
    request_data = request.get_json()
    
    df_predict = json_normalize(request_data)     
    bmi= predictBMI(df_predict,'knn')
    
    response = {}
    response['bmi'] = bmi[0]
    print(response)
    json_data = json.dumps(response)
    
    return json_data

@app.route('/getActivities', methods=['POST'])
def getActivities():
    print('getActivities')
    response = find_activity()
    
    return response


@app.route('/getRecipeBasedOnMeal', methods=['POST'])
def getRecipeBasedOnMeal():
    print('getRecipeBasedOnMeal call')
    request_data = request.get_json()
    
    reqData = json.loads(json.dumps(request_data), object_hook=customDecoder)  
    

    
    response= find_recipe_by_mealtype(reqData.mealtype)
    
    
    return response

@app.route('/getMotionBasedActivities', methods=['POST'])
def getMotionBasedActivities():
    print('getMotionBasedActivities call')
    request_data = request.get_json()
    
    reqData = json.loads(json.dumps(request_data), object_hook=customDecoder)  
    

    
    response= find_motion_activity(reqData.activity)
    
    
    return response

@app.route('/diabeticRisk', methods=['POST'])
def diabeticRisk():
    print('DiabeticRisk call')
    request_data = request.get_json()
    
    df_predict = json_normalize(request_data)     
    diabeticRisk= predictDiabeticRisk(df_predict)
    
    response = {}
    response['risk'] = diabeticRisk[0]
    print(response)
    json_data = json.dumps(response,cls=NpEncoder)
    
    return json_data


@app.route('/lifeStyleImprovement', methods=['POST'])
def lifeStyleImprovement():
    print('lifeStyleImprovement call')
    request_data = request.get_json()
    
    response = predictHealthRisk(json.dumps(request_data))
    
    print(response)
    #json_data = json.dumps(response)
    
    return response

@app.route('/drDetection', methods=['POST'])
def drDetection():
    print('drDetection')
    request_data = request.get_json()

    print (request_data)

    reqData = json.loads(json.dumps(request_data), object_hook=customDecoder)  
    
    resp = getRetinopathyLevel(reqData.image)
    
    print(resp)

    response = {}
    response['risk'] = resp[0]
    print(response)
    json_data = json.dumps(response,cls=NpEncoder)    
    #json_data = json.dumps(response)
    
    return json_data


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)
    
if __name__ == '__main__':
    app.run(debug = True,host='0.0.0.0', use_reloader=False, port=int(os.getenv('PORT', 5001)))  # run our Flask app , port=int(os.getenv('PORT', 5002))
   