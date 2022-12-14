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

# Removes Activities that have no trackpoints
REMOVE_ACTIVITY_WO_TRACKPOINT = f"""
DELETE FROM {TABLE_NAME_ACTIVITY} WHERE id NOT IN (SELECT f.activity_id FROM {TABLE_NAME_TRACKPOINT} f)
"""

# =========== TASK 2 ===========


# used for subtask 1 and 2
GET_USER_COUNT = f"""SELECT COUNT(*) FROM {TABLE_NAME_USER}"""
GET_ACTIVITY_COUNT = f"""SELECT COUNT(*) FROM {TABLE_NAME_ACTIVITY}"""
GET_TRACKPOINT_COUNT = f"""SELECT COUNT(*) FROM {TABLE_NAME_TRACKPOINT}"""
# query 1 = sum the rows above
# query 2 = divide get_activity_count and divide on get_user_count

# query 3 returns 20 users with most activities
GET_USERS_MOST_ACTIVITIES = f"""SELECT user_id, COUNT(*) AS count FROM {TABLE_NAME_ACTIVITY} GROUP BY user_id ORDER BY count DESC LIMIT 20"""

# query 4 gets users with transportation mode taxi
GET_USERS_WITH_TAXI = f"""SELECT DISTINCT user_id from {TABLE_NAME_ACTIVITY} WHERE transportation_mode="taxi";"""

# query 5
GET_TRANSPORTATION_MODE_COUNT = f""" SELECT transportation_mode, COUNT(*) as count FROM(SELECT transportation_mode FROM {TABLE_NAME_ACTIVITY} WHERE transportation_mode IS NOT NULL) AS alias GROUP BY transportation_mode;"""

# query 6a
GROUP_ACTIVITIES_BY_YEAR = f"""SELECT YEAR(start_date) AS year, COUNT(*) FROM {TABLE_NAME_ACTIVITY} GROUP BY year ORDER BY COUNT(*) DESC LIMIT 1;"""

# query 6b need to compare result with 6a
YEAR_MOST_HOURS = f"""SELECT YEAR(start_date) AS year, SUM(TIMEDIFF(start_date, end_date))as hours FROM {TABLE_NAME_ACTIVITY} GROUP BY year ORDER BY hours DESC LIMIT 1;"""

# query 7
# Returns the a table with Activity.start_date, Activity.end_date,
# TrackPoint.activity_id, TrackPoint.lat, TrackPoint.lon
FIND_TOTAL_DISTANCE_112 = f"""SELECT Activity.start_date, Activity.end_date, 
TrackPoint.activity_id, TrackPoint.lat, TrackPoint.lon FROM Activity INNER JOIN 
TrackPoint ON  Activity.id=TrackPoint.activity_id WHERE Activity.user_id = 112 AND
Activity.transportation_mode = 'walk';"""

# query 8
FIND_USERS_MOST_GAINED_ALTITUDE = f"""SELECT {TABLE_NAME_ACTIVITY}.user_id, SUM(gained_altitude_activity) * 0.3048 AS gained_altitude_total FROM (SELECT {TABLE_NAME_TRACKPOINT}.activity_id AS activity_id, GREATEST({TABLE_NAME_TRACKPOINT}.altitude - LAG({TABLE_NAME_TRACKPOINT}.altitude) OVER (ORDER BY {TABLE_NAME_TRACKPOINT}.id), 0) AS gained_altitude_activity FROM {TABLE_NAME_TRACKPOINT} WHERE altitude != -777) AS t LEFT JOIN {TABLE_NAME_ACTIVITY} on (t.activity_id = {TABLE_NAME_ACTIVITY}.id) GROUP BY {TABLE_NAME_ACTIVITY}.user_id ORDER BY gained_altitude_total DESC LIMIT 20;"""

# query 9
FIND_INVALID_ACTIVITIES = f"""SELECT DISTINCT user_id, COUNT(sub.activity_id) AS 'Invalid activity count' FROM (
SELECT activity_id, MINUTE(TIMEDIFF(lead(date_time) OVER(PARTITION BY activity_id ORDER BY date_time), date_time)) AS MinuteDiff FROM TrackPoint
) AS sub INNER JOIN Activity ON sub.activity_id = Activity.id WHERE MinuteDiff>=5 GROUP BY user_id;"""

# query 10
FIND_USERS_IN_FORBIDDEN_CITY = f"""SELECT user_id, lat, lon FROM (SELECT user_id, lat, lon, (lon BETWEEN 116.3 AND 116.4) AS lonBeijing, (lat BETWEEN 39.9 AND 40.1) AS latBeijing FROM {TABLE_NAME_ACTIVITY} INNER JOIN {TABLE_NAME_TRACKPOINT} ON {TABLE_NAME_ACTIVITY}.id = {TABLE_NAME_TRACKPOINT}.activity_id WHERE lat=40.088203) x WHERE lonBeijing=1;"""

# query 11
FIND_TRANSPORTATION_MODE_COUNT = f"""SELECT user_id, transportation_mode, COUNT(transportation_mode) AS count FROM Activity GROUP BY user_id, transportation_mode;"""
