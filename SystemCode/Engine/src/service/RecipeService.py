import sqlite3
from sqlite3 import Error
import sys
import os
import json
import psycopg2
from json import JSONEncoder

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
        print('Test')

    return conn


def select_ingredient_based_on_recipe(conn, rcp_code):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    result = cur.execute("SELECT distinct energy,totalpro,carb,fiber,ingr_code,ingr_descr_eng,\
                        mufa,chol,pufa,totalfat,sfa,water,totalsugars \
                         FROM tbl_recipe WHERE rcp_code =?",(rcp_code,))

    ing = [dict(zip([key[0] for key in cur.description], row)) for row in result]

    #r = [dict((cur.description[i][0], value) for i, value in enumerate(row)) for row in cur.fetchall()]

    return ing

def select_recipe_based_on_mealtype(conn, mealtype):
    """
    Query tasks by priority
    :param conn: the Connection object
    :param priority:
    :return:
    """
    cur = conn.cursor()
    result = cur.execute("SELECT distinct rcp_code,rcp_descr_eng FROM tbl_recipe_meal WHERE mealtype_cat = ?",(mealtype,))

    #rows = cur.fetchall()
    recipe = [dict(zip([key[0] for key in cur.description], row)) for row in result]

    #r = [dict((cur.description[i][0], value) for i, value in enumerate(row)) for row in cur.fetchall()]

    return recipe

def select_recipe_by_recipe_desc(conn, recpdesc):
    """
    Query tasks by priority
    :param conn: the Connection object
    :param priority:
    :return:
    """
    cur = conn.cursor()
    result = cur.execute("SELECT distinct rcp_code,rcp_descr_eng FROM tbl_recipe WHERE rcp_descr_eng like ?",('%'+recpdesc+'%',))

    #rows = cur.fetchall()
    recipe = [dict(zip([key[0] for key in cur.description], row)) for row in result]

    #r = [dict((cur.description[i][0], value) for i, value in enumerate(row)) for row in cur.fetchall()]

    return recipe


def find_recipe(recipe):
    module_path = os.path.abspath(os.path.join('../..'))
    database = module_path + "db/healthdb.db"
    
    # create a database connection
    conn = create_connection(database)
    with conn:
        print("1. Query task by recipe description:")
        result_row = select_recipe_by_recipe_desc(conn, recipe)
        
        json_output = json.dumps(result_row)
    return json_output
#         print("2. Query all tasks")
#         select_all_tasks(conn)

def find_recipe_by_mealtype(mealtype):
    module_path = os.path.abspath(os.path.join('../..'))
    database = module_path + "db/healthdb.db"
    
    # create a database connection
    conn = create_connection(database)
    with conn:
        print("1. Find Recipe by mealtype:")
        result_row = select_recipe_based_on_mealtype(conn, mealtype)
        recipesList = []
        
        for index in range(len(result_row)):
        
            recipes = Recipe()
            recipes.recipeCode = result_row[index]['rcp_code']
            recipes.recipeDescription = result_row[index]['rcp_descr_eng']
            recipes.mealtype = mealtype
            recipesList.append(recipes)
                
        
        json_output = json.dumps(recipesList,cls=Encoder)
        
    return json_output


def find_ingredient(recipeCode):
    module_path = os.path.abspath(os.path.join('../..'))
    database = module_path + "db/healthdb.db"
    
    # create a database connection
    conn = create_connection(database)
    with conn:
        print("1. Query task by recipe description:")
        result_row = select_ingredient_based_on_recipe(conn, recipeCode)
        ingredientList = []
        
        for index in range(len(result_row)):
        
            ingredients = Ingredient()
            ingredients.ingredientCode = result_row[index]['ingr_code']
            ingredients.ingredientDescription = result_row[index]['ingr_descr_eng']
            ingredients.recipeCode = recipeCode
            ingredientList.append(ingredients)
                
        
        json_output = json.dumps(ingredientList,cls=Encoder)
        
    return json_output
        
def calculate_ingredient(recipeCode):
    module_path = os.path.abspath(os.path.join('../..'))
    database = module_path + "db/healthdb.db"
    
    # create a database connection
    conn = create_connection(database)
    with conn:
        print("1. Query task by recipe description:")
        result_row = select_ingredient_based_on_recipe(conn, recipeCode)
        
        #print(result_row)
        ingredient = IngredientValue()
        ingredient.energy = sum(key['energy'] for key in result_row)              

        ingredient.totalpro=sum(key['totalpro'] for key in result_row)
        ingredient.carb = sum(key['carb'] for key in result_row)
        ingredient.fiber= sum(key['fiber'] for key in result_row) 
        ingredient.mufa = sum(key['mufa'] for key in result_row) 
        ingredient.chol = sum(key['chol'] for key in result_row)
        ingredient.pufa = sum(key['pufa'] for key in result_row)
        ingredient.totalfat=sum(key['totalfat'] for key in result_row) 
        ingredient.sfa= sum(key['sfa'] for key in result_row)
        ingredient.water= sum(key['water'] for key in result_row)
        ingredient.totalsugars=sum(key['totalsugars'] for key in result_row)
        
        jsonStr = json.dumps(ingredient.__dict__)
        return jsonStr


class Recipe:
    recipeCode = ''
    recipeDescription = ''
    mealtype = ''
    
    
class Ingredient:
    ingredientCode = ''
    ingredientDescription = ''
    recipeCode = ''

    
    def testing(self):
        print(self.ingredientCode)
        
class Encoder(JSONEncoder):
        def default(self, o):
            return o.__dict__
        
class IngredientValue:
    #def __init__(energy, totalpro, carb,fiber ,mufa ,chol ,pufa ,totalfat , sfa,water, totalsugars):
#     self.energy = energy
#     self.totalpro = totalpro
#     self.carb = carb
#     self.fiber = fiber
#     self.mufa = mufa
#     self.chol = chol   
#     self.pufa = pufa
#     self.totalfat = totalfat
#     self.sfa = sfa
#     self.water = water
#     self.totalsugars = totalsugars
    energy = 0      
    totalpro= 0
    carb = 0
    fiber= 0
    mufa = 0
    chol = 0
    pufa = 0
    totalfat =0
    sfa= 0
    water= 0
    totalsugars=0        

    
    def testing(self):
        print(self.energy)


#find_recipe('Coffee')
#print(calculate_ingredient('58160110'))
