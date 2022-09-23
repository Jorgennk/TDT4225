from logging.config import listen
from DbConnector import DbConnector
from tabulate import tabulate


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

    
    
    #read lines from files
    def read_from_file(self, path):
        f = open(path)
        lines = f.readlines()

        stripped_lines = []
        for line in lines[6:]:
            stripped_lines.append(self.cut_newline(line))
        
        return stripped_lines

        

    def create_table(self, table_name):
        query = """CREATE TABLE IF NOT EXISTS %s (
                   id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
                   name VARCHAR(30))
                """
        # This adds table_name to the %s variable and executes the query
        self.cursor.execute(query % table_name)
        self.db_connection.commit()


    def cut_newline(self, input_line):

        input_line = input_line.rstrip("\n")


        return input_line

    def get_labeled_ids(self):

        f = open("dataset\labeled_ids.txt")
        lines = f.readlines()

        labeled_ids = []
        for line in lines:
            labeled_ids.append(self.cut_newline(line))

        return labeled_ids

    def retrieve_list(self) -> list:
        #This method retrives a list of the numbers (folder names) "XXX" which will be used as user ID
        import os 
        directory_list = list()
        for root, dirs, files in os.walk("./dataset/Data/", topdown=False, followlinks=False):
            for name in dirs:
                try:
                    #Simple check to see if they are nuers
                    int(name)
                    directory_list.append(name)
                except:
                    pass
                
        labeled_ids = self.get_labeled_ids()
        for label in labeled_ids:
            if label not in directory_list:
                labeled_ids.remove(label)

        return labeled_ids

    def get_activity(self, labeled_ids):
        print(f"HER @@@@@@@{labeled_ids}")
        for user in labeled_ids:
            path = f"./dataset/Data/{user}/labels.txt"
            activity = self.read_from_file(path)
            return activity

        






    def insert_data(self, table_name):
        names = self.retrieve_list()
        for name in names:
            # Take note that the name is wrapped in '' --> '%s' because it is a string,
            # while an int would be %s etc
            query = "INSERT INTO %s (name) VALUES ('%s')"
            self.cursor.execute(query % (table_name, name))
        self.db_connection.commit()



    def insert_data_name(self, table_name):
        names = self.retrieve_list()
        for name in names:
            # Take note that the name is wrapped in '' --> '%s' because it is a string,
            # while an int would be %s etc
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
    try:
        program = Imsdal()
        program.create_table(table_name="User")
        
        content = program.retrieve_list()
        program.insert_data(table_name="User")
        _ = program.fetch_data(table_name="User")
        program.drop_table(table_name="User")
        # Check that the table is dropped
        program.show_tables()
    except Exception as e:
        print("ERROR: Failed to use database:", e)
    finally:
        if program:
            program.connection.close_connection()



program = Imsdal()
print(program.read_from_file("dataset\\Data\\000\Trajectory\\20081023025304.plt"))
"""
if __name__ == '__main__':
    main()
"""

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