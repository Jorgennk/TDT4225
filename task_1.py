from logging.config import listen
from DbConnector import DbConnector
from tabulate import tabulate
import datetime
import os 



class Table:

    def __init__(self, name, create_string) -> None:
        self.name = name
        self.create_string = create_string
        self.content = []

    def set_content(self, user_id, ) -> None:

        self.content.append(new_content)


class Imsdal:
    

    def __init__(self) -> None:
        self.connection = DbConnector()
        self.db_connection = self.connection.db_connection
        self.cursor = self.connection.cursor

    
    def cut_newline(self, input_line) -> str:
    
        input_line = input_line.rstrip("\n")

        return input_line
    
    #read lines from trajectories
    def read_from_trajectory(self, path) -> list:
        f = open(path)
        lines = f.readlines()

        stripped_lines = []
        for line in lines[6:]:
            stripped_lines.append(self.cut_newline(line))
        
        return stripped_lines


    #Pretty similar to above, check if this can be done easier
    def read_from_labels(self, path) -> list:
        f = open(path)
        lines = f.readlines()

        stripped_lines = []
        for line in lines:
            stripped_lines.append(self.cut_newline(line))
        
        return stripped_lines



    def create_table(self, table_name):
        query = """CREATE TABLE IF NOT EXISTS %s (
                   id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
                   user_id INT NOT NULL,
                   start_date DATETIME,
                   end_date DATETIME,
                   name VARCHAR(30),
                   FOREIGN KEY (user_id) REFERENCES User(id))
                """
        # This adds table_name to the %s variable and executes the query
        self.cursor.execute(query % table_name)
        self.db_connection.commit()


    #Returns labeled ids as a list.
    def get_labeled_ids(self):

        f = open("dataset\labeled_ids.txt")
        lines = f.readlines()

        labeled_ids = []
        for line in lines:
            labeled_ids.append(self.cut_newline(line))

        return labeled_ids

    #This method retrives a list of the numbers (folder names) "XXX" which will be used as user ID
    def retrieve_list(self, filter=True) -> list:
        
        directory_list = list()
        for root, dirs, files in os.walk("./dataset/Data/", topdown=False, followlinks=False):
            for name in dirs:
                try:
                    int(name) # Simple check to see if name is number
                    directory_list.append(name)
                except:
                    pass
       
        labeled_ids = self.get_labeled_ids()
        if filter:
            for label in labeled_ids:
                if label not in directory_list:
                    labeled_ids.remove(label)

        return labeled_ids

    def insert_users(self, list_of_users):
        labeled_users = self.retrieve_list()
        query = "INSERT INTO User (id, has_labels) VALUES (%s,%s)"
        to_be_inserted = []
        for user in list_of_users:
            to_be_inserted.append((user, user in labeled_users))
        print(to_be_inserted)
        try:
            self.cursor.executemany(query, to_be_inserted)
            self.db_connection.commit()
        except:
            self.db_connection.rollback()


 
    def get_activity(self, labeled_ids):
        content = []
        for user in labeled_ids:
            #print(user)
            path = f"./dataset/Data/{user}/labels.txt"
            content.append((user, self.format_activity(self.read_from_trajectory(path))))
        
        return content

    #Basically just puts the different fields in into separated list
    #so they are easier to work with
    def format_activity(self, list_of_entries) -> list:

        formatted = []
        for line in list_of_entries:
            #Split on tabs
            formatted.append(line[1].split("\t"))

        return formatted

    

    def insert_data(self, table_name, names, user_id):
        name_tuples = []
        for name in names:
            name_tuples.append(tuple(user_id, name))
        query = f"INSERT INTO {table_name} (user_id, start_date, end_date, name) VALUES (%s,%s,%s)"
        #print(name_tuples)
        self.cursor.executemany(query, name_tuples)
        self.db_connection.commit()



    def insert_data_name(self, table_name, list_of_users):
        for name in list_of_users:
            # Take note that the name is wrapped in '' --> '%s' because it is a string,
            # while an int would be %s etc
            pass
        query = "INSERT INTO %s (name) VALUES ('%s')"
        self.cursor.execute(query % (table_name, name))
        self.db_connection.commit()


    def fetch_data(self, table_name):
        query = "SELECT * FROM %s"
        self.cursor.execute(query % table_name)
        rows = self.cursor.fetchall()
        print("Data from table %s, raw format:" % table_name)
        print(rows)
        # Using tabulate to show the table in a nice way
        print("Data from table %s, tabulated:" % table_name)
        print(tabulate(rows, headers=self.cursor.column_names))
        return rows

    def drop_table(self, table_name):
        print("Dropping table %s..." % table_name)
        query = "DROP TABLE %s"
        self.cursor.execute(query % table_name)

    def show_tables(self):
        self.cursor.execute("SHOW TABLES")
        rows = self.cursor.fetchall()
        print(tabulate(rows, headers=self.cursor.column_names))



def main():
    program = None
    program = Imsdal()
    program.create_table(table_name="Activity")

    users = program.retrieve_list(filter = False)
    activity = program.get_activity(users)

    for element in activity:
        user = element[0]
        content = element[1]
        program.insert_data("Activity", content, user)
    program.insert_users(users)
    
    #print(program.get_trackpoints(users[1]))
        


if __name__ == '__main__':
    main()

"""
f = open("./dataset/Data/000/Trajectory/20081023025304.plt", "r")
Lines = f.readlines()


count = 0
# Strips the newline character

content = [["X", "Y", "Z", "Date"]]

for line in Lines:
    count += 1
    if count > 6:
        tmp_line = line.split(",")
        content.append([tmp_line[0], tmp_line[1], tmp_line[3], tmp_line[4]])
        #print(line.split(","))
        if count > 20:
            break


print(*content, sep="\n")
if __name__ == '__main__':
    main()
"""