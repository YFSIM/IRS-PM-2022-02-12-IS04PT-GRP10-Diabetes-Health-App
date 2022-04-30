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
        print(db_file)
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
        print('Test')

    return conn


def select_activity(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    result = cur.execute("SELECT distinct activity \
                         FROM tbl_activity")

    act = [dict(zip([key[0] for key in cur.description], row)) for row in result]

    return act

def select_met_based_on_motion_activity(conn, activity,motion):
    """
    Query tasks by priority
    :param conn: the Connection object
    :param priority:
    :return:
    """
    cur = conn.cursor()
    result = cur.execute("SELECT specificmotion, mets FROM tbl_activity WHERE activity = ? and specificmotion=?",(activity,motion,))

    #rows = cur.fetchall()
    met = [dict(zip([key[0] for key in cur.description], row)) for row in result]

    #r = [dict((cur.description[i][0], value) for i, value in enumerate(row)) for row in cur.fetchall()]

    return met

def select_specific_activity(conn, activity):
    """
    Query tasks by priority
    :param conn: the Connection object
    :param priority:
    :return:
    """
    cur = conn.cursor()
    result = cur.execute("SELECT specificmotion, mets FROM tbl_activity WHERE activity = ?",(activity,))

    #rows = cur.fetchall()
    motion = [dict(zip([key[0] for key in cur.description], row)) for row in result]

    #r = [dict((cur.description[i][0], value) for i, value in enumerate(row)) for row in cur.fetchall()]

    return motion

def find_met(activity,motion):
    module_path = os.path.abspath(os.path.join(''))
    database = module_path + "db/healthdb.db"
    
    #print(activity)
    # create a database connection
    conn = create_connection(database)
    with conn:
        #print("1. Find Activity:")
        result_row = select_met_based_on_motion_activity(conn,activity,motion)
        

        json_output = json.dumps(result_row)
        #print(json_output)
    return json_output

def find_activity():
    module_path = os.path.abspath(os.path.join(''))
    database = module_path + "db/healthdb.db"
    
    # create a database connection
    conn = create_connection(database)
    with conn:
        
        result_row = select_activity(conn)
        
        json_output = json.dumps(result_row)

    return json_output

def find_motion_activity(activityDesc):
    module_path = os.path.abspath(os.path.join(''))
    database = module_path + "db/healthdb.db"
    print(database)
    # create a database connection
    conn = create_connection(database)
    with conn:
        
        result_row = select_specific_activity(conn, activityDesc)
        activityList = []
        
        
        for index in range(len(result_row)):
        
            activityC = Activity()
            activityC.specificmotion = result_row[index]['SPECIFICMOTION']
            activityC.met = result_row[index]['METs']
            activityC.activity = activityDesc
            activityList.append(activityC)
                
        
        json_output = json.dumps(activityList,cls=Encoder)
        
    return json_output


class Activity:
    activity = ''
    specificmotion = ''
    met = 0

    
    def testing(self):
        print(self.met)
        
class Encoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
      


#find_recipe('Coffee')
#print(find_met('bicycling','bicycling, general'))