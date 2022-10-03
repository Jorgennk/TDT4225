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

#query 3
GET_USERS_MOST_ACTIVITIES = f"""SELECT user_id, COUNT(*) AS count FROM {TABLE_NAME_ACTIVITY} GROUP BY user_id ORDER BY count DESC LIMIT 20"""



