# importing the requests library
import requests
import json

# defining the api-endpoint
API_ENDPOINT_GET_MOTION = "http://18.141.200.11:5001/getMotionBasedActivities"
API_ENDPOINT_GET_ACTIVITY = "http://18.141.200.11:5001/getActivities"
API_ENDPOINT_GET_RECIPE_MEALTYPE = "http://18.141.200.11:5001/getRecipeBasedOnMeal"
API_ENDPOINT_GET_DIABETIC_RISK = "http://18.141.200.11:5001/diabeticRisk"
API_ENDPOINT_GET_LIFE_IMPROVEMENT = "http://18.141.200.11:5001/lifeStyleImprovement"

# your API key here
API_KEY = "XXXXXXXXXXXXXXXXX"



# data to be sent to api
# data = {'api_dev_key':API_KEY,
#         'api_option':'paste',
#         'api_paste_code':source_code,
#         'api_paste_format':'python'}

#input is activity e.g bicycling
#return list of obj with property specificmotion<string>,met<float>,activity<string>
#sample getMotionBasedActivities('bicycling')
def getMotionBasedActivities(activityType):
    data = {'activity': activityType}

    try:
        # sending post request and saving response as response object
        r = requests.post(url = API_ENDPOINT_GET_MOTION, json = data)

        # extracting response text
        pastebin_url = r.text
        objresponse = json.loads(pastebin_url)
    except Exception as e:
        print(e)
        return ''
    return objresponse
    

#input is blank
#return list of obj with property ACTIVITY<string>
#sample getActivities()
def getActivities():
    
    try:
        # sending post request and saving response as response object
        r = requests.post(url = API_ENDPOINT_GET_ACTIVITY)

        # extracting response text
        pastebin_url = r.text
        objresponse = json.loads(pastebin_url)
    except Exception as e:
        print(e)
        return ''
    
    return objresponse

#input is activity e.g breakfast,dinner,lunch
#return list of obj with property recipeCode<int>,recipeDescription<string>,mealtype<string>
#sample getRecipeBasedOnMeal('breakfast')
def getRecipeBasedOnMeal(mealtype):
    data = {'mealtype': mealtype}

    try:
        # sending post request and saving response as response object
        r = requests.post(url = API_ENDPOINT_GET_RECIPE_MEALTYPE, json = data)

        # extracting response text
        pastebin_url = r.text
        objresponse = json.loads(pastebin_url)
    except Exception as e:
        print(e)
        return ''
    return objresponse

#input are HighBP<int>,HighChol<int>,BMI<int>,Smoker<int>,Stroke<int>,HeartDiseaseorAttack<int>,
#PhysActivity<int>, Fruits<int>,Veggies<int>, HvyAlcoholConsump<int>, MentHlth<int>, PhysHlth<int>,
#DiffWalk<int>, Sex<int>, Age<int>
#return obj with property risk<int>
#sample getDiabeticRisk(1,1,30,1,1,1,1,0,1,0,5,30,0,1,50)
def getDiabeticRisk(HighBP, HighChol,BMI,Smoker,Stroke,HeartDiseaseorAttack,PhysActivity,Fruits,Veggies,HvyAlcoholConsump,MentHlth,PhysHlth,DiffWalk,Sex,Age):
    data = {'HighBP': HighBP, 'HighChol':HighChol,'BMI':BMI, 'Smoker':Smoker,'Stroke':Stroke,'HeartDiseaseorAttack':HeartDiseaseorAttack, \
            'PhysActivity':PhysActivity,'Fruits':Fruits,'Veggies':Veggies,'HvyAlcoholConsump':HvyAlcoholConsump,'MentHlth':MentHlth,'PhysHlth':PhysHlth,'DiffWalk':DiffWalk,'Sex':Sex,'Age':Age}

    try:
        # sending post request and saving response as response object
        r = requests.post(url = API_ENDPOINT_GET_DIABETIC_RISK, json = data)

        # extracting response text
        pastebin_url = r.text
        objresponse = json.loads(pastebin_url)
    except Exception as e:
        print(e)
        return ''
    return objresponse

#input are age<int>,height<int-cm>,weight<int-kg>,activity<string>,motion<string-from specificmotion from getMotionBasedActivities>,noofexerciseaweek<int>,
#minofexercise<int-eachtime>, breakfast<String-recipecode from getRecipeBasedOnMeal>,lunch<String-recipecode from getRecipeBasedOnMeal>,
#dinner<String-recipecode from getRecipeBasedOnMeal>
#return obj with property breakfastMealAdvice<string>,lunchMealAdvice<string>,dinnerMealAdvice<string>,physicalExerciseAdvice<string> 
#sample getImprovementSuggestion(33,168,76,'bicycling','bicycling, mountain, competitive, racing',3,30,'172791998','5234','58160110')
def getImprovementSuggestion(age, height,weight,activity,motion,noofexerciseaweek,minofexercise,breakfast,lunch,dinner):
    data = {'age': age, 'height':height,'weight':weight, 'activity':activity,'motion':motion,'noofexerciseaweek':noofexerciseaweek, \
            'minofexercise':minofexercise,'breakfast':breakfast,'lunch':lunch,'dinner':dinner}

    try:
        # sending post request and saving response as response object
        r = requests.post(url = API_ENDPOINT_GET_LIFE_IMPROVEMENT, json = data)

        # extracting response text
        pastebin_url = r.text
        objresponse = json.loads(pastebin_url)
    except Exception as e:
        print(e)
        return ''
    return objresponse

test = getImprovementSuggestion(33,168,76,'bicycling','bicycling, mountain, competitive, racing',3,30,'172791998','5234','58160110')
print(test)