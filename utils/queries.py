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
                   name VARCHAR(30),
                   FOREIGN KEY (user_id) REFERENCES User(id))
                """
INSERT_ACTIVITY = f"INSERT INTO {TABLE_NAME_ACTIVITY} (user_id, start_date, end_date, name) VALUES (%s,%s,%s)"

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