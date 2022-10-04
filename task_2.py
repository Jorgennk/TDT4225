from unittest import result
from utils.db_connector import DbConnector
import utils.db as db
import utils.queries as queries
import pandas as pd
import tabulate as tabulate
import numpy as np

def get_count(query: str, _db: DbConnector):
    return db.execute_query_get_result(_db, query)[0][0]

def task1(db_conn: DbConnector):
    user_count = get_count(queries.GET_USER_COUNT, db_conn)
    activity_count = get_count(queries.GET_ACTIVITY_COUNT, db_conn)
    trackpoint_count = get_count(queries.GET_TRACKPOINT_COUNT, db_conn)
    print(f"user count: {user_count}, activity count: {activity_count}, trackpoint count: {trackpoint_count}, total: {user_count+activity_count+trackpoint_count}")

def task2(db_conn: DbConnector):
    activity_count = get_count(queries.GET_ACTIVITY_COUNT, "Getting activities..,", db_conn)
    user_count = get_count(queries.GET_USER_COUNT, "Getting user count..", db_conn)
    print(f"Average activity for user is activity count/user count = {round(activity_count/user_count, 2)}")

def task3(db_conn: DbConnector):
    query = queries.GET_USERS_MOST_ACTIVITIES
    result = db.execute_query_get_result(db_conn, query)
    df = pd.DataFrame(result, columns=['user', 'activity_count'])
    print("The 20 users with the most activities are: ")
    print(df)

def task4(db_conn: DbConnector):
    query = queries.GET_USERS_WITH_TAXI
    result = db.execute_query_get_result(db_conn, query) 
    df = pd.DataFrame(result, columns=['Users'])
    print("Users that have taken taxi")
    print(df)

def task5(db_conn: DbConnector):
    query = queries.GET_TRANSPORTATION_MODE_COUNT
    result = db.execute_query_get_result(db_conn, query)
    df = pd.DataFrame(result, columns=['Transportation mode', "Count"])
    print("The use of each transportation mode is as following: ")
    print(df)

def task6a(db_conn: DbConnector):
    query = queries.GROUP_ACTIVITIES_BY_YEAR
    result = db.execute_query_get_result(db_conn, query)
    df = pd.DataFrame(result, columns=["Year", "Activity count"])
    print("The year with the most activities is: ")
    print(df)

def task6b(db_conn: DbConnector):
    query6a = queries.GROUP_ACTIVITIES_BY_YEAR
    query6b = queries.YEAR_MOST_HOURS
    result_6b = db.execute_query_get_result(db_conn, query6b)[0][0]
    result_6a = db.execute_query_get_result(db_conn, query6a)[0][0]
    print("The year with most tracked hours is ")
    print(result_6b)
    if result_6a == result_6b:
        print("The year with the most activities is also the same as the year with the most tracked hours")
    else:
        print("The year with the most tracked activities is not the same as with the most tracked hours")

def distance(in_lat, in_long, in_lat2, in_long2):
    lat_dist = abs(in_lat2 - in_lat)
    long_dist = abs(in_long2 - in_long)
    print(f"lat1: {in_lat}, lon1: {in_long} lat2: {in_lat2}, lon2: {in_long2}")
    
    euclidean_dist = np.sqrt(lat_dist**2 + long_dist**2)
    print(f"Distance: {euclidean_dist}")
    return euclidean_dist    

def task_7(db_conn: DbConnector):
    user_count = get_count(queries.GET_USER_COUNT, db_conn)
    query = queries.FIND_TOTAL_DISTANCE_112
    result = db.execute_query_get_result(db_conn, query)
    df = pd.DataFrame(result, columns=['start_date', 'end_date', 'activity_id', 'lat', 'lon',])

    #df['dist'] = mt.sqrt((df['lat']-df['lat'].shift())**2 + (df['lon']- df['lon'].shift())**2)
    #df['dist'] = df.apply(lambda row: mt.sqrt((df['lat']-df['lat'].shift())**2 + (df['lon']- df['lon'].shift())**2), axis = 1)

    df['dist'] = df.apply(lambda row : distance(row['lat'], row['lon'], row.shift(periods=1)['lat'], row.shift(periods)['lon']), axis = 1)
    print(df.head())

def task8(db_conn: DbConnector):
    query = queries.FIND_USERS_MOST_GAINED_ALTITUDE
    result = db.execute_query_get_result(db_conn, query)
    df = pd.DataFrame(result, columns=['User:     ', "Gained altitude:"])
    print("The 20 users with the most gained altitude are: ")
    print(df)

def task10(db_conn: DbConnector):
    query = queries.FIND_USERS_IN_FORBIDDEN_CITY
    result = db.execute_query_get_result(db_conn, query)
    df = pd.DataFrame(result, columns=["User:  ", "Lat:  ", "Long:  "])
    print("The users that have been in the forbidden city in Beijing are:  ")
    print(df)

def main():
    db_conn = DbConnector()
    #task1(db_conn)
    #task2(db_conn)
    #task3(db_conn)
    #task4(db_conn)
    #task5(db_conn)
    #task6a(db_conn)
    #task6b(db_conn)
    #task_7(db_conn)
    task8(db_conn)
    task10(db_conn)
    db_conn.close_connection()
        
if __name__ == "__main__":
    main()
