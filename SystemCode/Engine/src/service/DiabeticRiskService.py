import sys
import os
import pandas as pd

import pickle

def dt_lsmodel():
    module_path = os.path.abspath(os.path.join('../..'))
    filepath = module_path  + 'model/' + 'dbtmodel.pkl'
    print(filepath)


    decision_tree_model_pkl = open(filepath, 'rb')
    decision_tree_model = pickle.load(decision_tree_model_pkl)
    return decision_tree_model

    
def predictDiabeticRisk(input):
    model = dt_lsmodel()
    predict_value = model.predict(input)
    return predict_value

def test():
    df_predict = pd.read_csv("dbtmodel_test.csv")
    print(predictDiabeticRisk(df_predict))
    
