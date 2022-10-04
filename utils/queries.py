# Table names
TABLE_NAME_ACTIVITY = "Activity"
TABLE_NAME_USER = "User"
TABLE_NAME_TRACKPOINT = "TrackPoint"

# User
CREATE_TABLE_USER = f"""CREATE TABLE IF NOT EXISTS {TABLE_NAME_USER} (
                    id VARCHAR(30) NOT NULL PRIMARY KEY,
                    has_labels TINYINT)
                """
INSERT_USER = f"INSERT INTO {TABLE_NAME_USER} (id, has_labels) VALUES (%s,%s)"

# Activity
CREATE_TABLE_ACTIVITY = f"""CREATE TABLE IF NOT EXISTS {TABLE_NAME_ACTIVITY} (
                   id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
                   user_id VARCHAR(30) NOT NULL,
                   start_date DATETIME,
                   end_date DATETIME,
                   transportation_mode VARCHAR(30),
                   FOREIGN KEY (user_id) REFERENCES User(id))
                """
INSERT_ACTIVITY = f"INSERT INTO {TABLE_NAME_ACTIVITY} (end_date, start_date, transportation_mode, user_id) VALUES " \
                  f"(%s,%s,%s,%s)"

# TrackPoint
CREATE_TABLE_TRACKPOINT = f"""CREATE TABLE IF NOT EXISTS {TABLE_NAME_TRACKPOINT} (
                    id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
                    activity_id INT NOT NULL,
                    lat DOUBLE NOT NULL,
                    lon DOUBLE NOT NULL,
                    altitude INT,
                    date_time DATETIME,
                    FOREIGN KEY (activity_id) REFERENCES {TABLE_NAME_ACTIVITY}(id))
                """
INSERT_TRACKPOINT = f"INSERT INTO {TABLE_NAME_TRACKPOINT} (lat, lon, altitude, date_time, activity_id) VALUES (%s,%s,%s,%s,%s)"

#Removes Activities that have no trackpoints 
REMOVE_ACTIVITY_WO_TRACKPOINT = f"""DELETE FROM {TABLE_NAME_ACTIVITY} WHERE id NOT IN (SELECT f.activity_id FROM {TABLE_NAME_TRACKPOINT} f)"""


#til query1 og 2 
GET_USER_COUNT = f"""SELECT COUNT(*) FROM {TABLE_NAME_USER}"""
GET_ACTIVITY_COUNT = f"""SELECT COUNT(*) FROM {TABLE_NAME_ACTIVITY}"""
GET_TRACKPOINT_COUNT = f"""SELECT COUNT(*) FROM {TABLE_NAME_TRACKPOINT}"""
#query 1 = summer alle ovenfor
#query 2 = ta get_activity_count og del på get_user_count

#query 3 returns 20 users with most activities
GET_USERS_MOST_ACTIVITIES = f"""SELECT user_id, COUNT(*) AS count FROM {TABLE_NAME_ACTIVITY} GROUP BY user_id ORDER BY count DESC LIMIT 20"""

#query4 gets users with transportation mode taxi
GET_USERS_WITH_TAXI = f"""SELECT DISTINCT user_id from {TABLE_NAME_ACTIVITY} WHERE transportation_mode="taxi";"""

#query5 Get 
GET_TRANSPORTATION_MODE_COUNT = f""" SELECT transportation_mode, COUNT(*) as count FROM(SELECT transportation_mode FROM {TABLE_NAME_ACTIVITY} WHERE transportation_mode IS NOT NULL) AS alias GROUP BY transportation_mode;"""

#query6a
GROUP_ACTIVITIES_BY_YEAR = f"""SELECT YEAR(start_date) AS year, COUNT(*) FROM {TABLE_NAME_ACTIVITY} GROUP BY year ORDER BY COUNT(*) DESC LIMIT 1;"""

#query6b need to compare result with 6a
YEAR_MOST_HOURS = f"""SELECT YEAR(start_date) AS year, SUM(TIMEDIFF(start_date, end_date))as hours FROM {TABLE_NAME_ACTIVITY} GROUP BY year ORDER BY hours DESC LIMIT 1;"""

#query7
#Returns the a table with Activity.start_date, Activity.end_date, 
#TrackPoint.activity_id, TrackPoint.lat, TrackPoint.lon

FIND_TOTAL_DISTANCE_112 = f"""SELECT Activity.start_date, Activity.end_date, 
TrackPoint.activity_id, TrackPoint.lat, TrackPoint.lon FROM Activity INNER JOIN 
TrackPoint ON  Activity.id=TrackPoint.activity_id WHERE Activity.user_id = 112 AND
Activity.transportation_mode = 'walk';"""




