from utils.db_connector import DbConnector
from tabulate import tabulate
from haversine import haversine


class Queries:

    def __init__(self):
        self.connection = DbConnector()
        self.db_connection = self.connection.db_connection
        self.cursor = self.connection.cursor



       

