from unittest.util import sorted_list_difference
from utils.db_connector import DbConnector
from typing import Union
import utils.db as db
import utils.queries as queries
import pandas as pd
import numpy as np


def get_count(query: str, _db: DbConnector, msg: str = None):
    if msg is not None:
        print(msg)
    return db.execute_query_get_result(_db, query, print_success=False)[0][0]


def print_task_number(no: Union[str, int]):
    print(f"\n[============== TASK {no} ==============]\n")


def task1(db_conn: DbConnector):
    print_task_number(1)
    user_count = get_count(queries.GET_USER_COUNT, db_conn)
    activity_count = get_count(queries.GET_ACTIVITY_COUNT, db_conn)
    trackpoint_count = get_count(queries.GET_TRACKPOINT_COUNT, db_conn)
    print(f"user count: {user_count}, activity count: {activity_count}, trackpoint count: {trackpoint_count}, total: {user_count+activity_count+trackpoint_count}")


def task2(db_conn: DbConnector):
    print_task_number(2)
    activity_count = get_count(queries.GET_ACTIVITY_COUNT, db_conn, "Getting activities..,")
    user_count = get_count(queries.GET_USER_COUNT, db_conn, "Getting user count..")
    print(f"Average activity for user is activity count/user count = {round(activity_count/user_count, 2)}")


def task3(db_conn: DbConnector):
    print_task_number(3)
    query = queries.GET_USERS_MOST_ACTIVITIES
    result = db.execute_query_get_result(db_conn, query, print_success=False)
    df = pd.DataFrame(result, columns=['user', 'activity_count'])
    print("The 20 users with the most activities are: ")
    print(df)


def task4(db_conn: DbConnector):
    print_task_number(4)
    query = queries.GET_USERS_WITH_TAXI
    result = db.execute_query_get_result(db_conn, query, print_success=False)
    df = pd.DataFrame(result, columns=['Users'])
    print("Users that have taken taxi")
    print(df)


def task5(db_conn: DbConnector):
    print_task_number(5)
    query = queries.GET_TRANSPORTATION_MODE_COUNT
    result = db.execute_query_get_result(db_conn, query, print_success=False)
    df = pd.DataFrame(result, columns=['Transportation mode', "Count"])
    print("The use of each transportation mode is as following: ")
    print(df)


def task6a(db_conn: DbConnector):
    print_task_number("6a")
    query = queries.GROUP_ACTIVITIES_BY_YEAR
    result = db.execute_query_get_result(db_conn, query, print_success=False)
    df = pd.DataFrame(result, columns=["Year", "Activity count"])
    print("The year with the most activities is: ")
    print(df)


def task6b(db_conn: DbConnector):
    print_task_number("6b")
    query6a = queries.GROUP_ACTIVITIES_BY_YEAR
    query6b = queries.YEAR_MOST_HOURS
    result_6b = db.execute_query_get_result(db_conn, query6b, print_success=False)[0][0]
    result_6a = db.execute_query_get_result(db_conn, query6a, print_success=False)[0][0]
    print("The year with most tracked hours is ")
    print(result_6b)
    if result_6a == result_6b:
        print("The year with the most activities is also the same as the year with the most tracked hours")
    else:
        print("The year with the most tracked activities is not the same as with the most tracked hours")


def distance(in_lat, in_long, in_lat2, in_long2):
    lat_dist = abs(in_lat2 - in_lat)
    long_dist = abs(in_long2 - in_long)
    #print(f"lat1: {in_lat}, lon1: {in_long} lat2: {in_lat2}, lon2: {in_long2}")
    
    #Assuming that the Earth is a sphere with a circumference of 40075 km.
    #adjust for earth curvature
    #This adjusts for 1 degree of latitude/longitude
    len_lat = 111.32 #km
    len_lon = 40075* np.cos( in_lat ) / 360 #km
    euclidean_dist = np.sqrt((lat_dist*len_lat)**2 + (long_dist*len_lon)**2)


    #print(f"Distance: {euclidean_dist} km")
    return euclidean_dist    


#In hindsight, this could probably be done in the query, HA
def task_7(db_conn: DbConnector):
    print_task_number(7)
    query = queries.FIND_TOTAL_DISTANCE_112
    result = db.execute_query_get_result(db_conn, query)
    df = pd.DataFrame(result, columns=['start_date', 'end_date', 'activity_id', 'lat', 'lon',])
    
    #print the eaculidean distance between the trackpoints
    print("Finding distance walked for user 112...")
    last = None

    #list of different distances, always start with 0 and not starting/ending points between 
    # activities
    distance_sorted = [] 
    list_of_distance = [] #Used for tmp storage of distances
    for e in df.itertuples():
        if last:
            #Create new list if we change activity
            if last_activity_id != e.activity_id:
                distance_sorted.append(list_of_distance)
                list_of_distance = []
                list_of_distance.append(0)
            else:
                list_of_distance.append(distance(e[4], e[5], last[4], last[5]))
        else:
            list_of_distance.append(0)
        last = e
        last_activity_id = e[3]
    
    #Sum distances for different activities
    sum_of_distance = 0
    for item in distance_sorted:
        sum_of_distance += sum(item)
    print(f"Total distance walked for user_id 112 (in km): {sum_of_distance}")


def task8(db_conn: DbConnector):
    print_task_number(8)
    query = queries.FIND_USERS_MOST_GAINED_ALTITUDE
    result = db.execute_query_get_result(db_conn, query, print_success=False)
    df = pd.DataFrame(result, columns=['User:     ', "Gained altitude:"])
    print("The 20 users with the most gained altitude are: ")
    print(df)


def task9(db_conn: DbConnector):
    print_task_number(9)
    query = queries.FIND_INVALID_ACTIVITIES
    result = db.execute_query_get_result(db_conn, query, print_success=False)
    df = pd.DataFrame(result, columns=['User ID:     ', "Invalid activity count:"])
    print(df)


def task10(db_conn: DbConnector):
    print_task_number(10)
    print("We search for users with lat in [39.9, 40.1] and lon in [116.3, 116.4].")
    query = queries.FIND_USERS_IN_FORBIDDEN_CITY
    result = db.execute_query_get_result(db_conn, query, print_success=False)
    df = pd.DataFrame(result, columns=["User:  ", "Lat:  ", "Long:  "])
    print("The users that have been in the forbidden city in Beijing are:  ")
    print(df)
    print("\nSince only 1 user was in Beijing, we choose to show all records with lat and lon coordinates.")


def task11(db_conn: DbConnector):
    print_task_number(11)
    print("We first retrieve a list of users, transportation mode, and the number of times they have been recorded using that transportation mode.")
    print("We then use python to find the most common transportation modes for each user.")
    print("Using dictionaries, we can achieve linear complexity O(N) for the Python code, where N is the number of labeled users.")
    query = queries.FIND_TRANSPORTATION_MODE_COUNT
    result_dict: dict = {}
    result = db.execute_query_get_result(db_conn, query, print_success=False)
    for row in result:
        uid: str = row[0]
        count: int = row[2]
        if uid not in result_dict:
            result_dict[uid] = row
            continue
        if result_dict[uid][2] < count:
            result_dict[uid] = row
    df = pd.DataFrame(list(result_dict.values()), columns=["user_id:  ", "transportation_mode:  ", "count:  "])
    print("\nThe most common transportation mode for each user (with counts) is:")
    print(df)

def main():
    db_conn = DbConnector()
    task1(db_conn)
    task2(db_conn)
    task3(db_conn)
    task4(db_conn)
    task5(db_conn)
    task6a(db_conn)
    task6b(db_conn)
    task_7(db_conn)
    task8(db_conn)
    task9(db_conn)
    task10(db_conn)
    task11(db_conn)
    db_conn.close_connection()


if __name__ == "__main__":
    main()
