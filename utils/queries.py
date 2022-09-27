# Table names
TABLE_NAME_ACTIVITY = "Activity"
TABLE_NAME_USER = "User"

# User
INSERT_USER = f"INSERT INTO {TABLE_NAME_USER} (id, has_labels) VALUES (%s,%s)"

# Activity
CREATE_TABLE_ACTIVITY = f"""CREATE TABLE IF NOT EXISTS {TABLE_NAME_ACTIVITY} (
                   id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
                   user_id INT NOT NULL,
                   start_date DATETIME,
                   end_date DATETIME,
                   name VARCHAR(30),
                   FOREIGN KEY (user_id) REFERENCES User(id))
                """
INSERT_ACTIVITY = f"INSERT INTO {TABLE_NAME_ACTIVITY} (user_id, start_date, end_date, name) VALUES (%s,%s,%s)"

