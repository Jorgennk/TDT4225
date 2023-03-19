from utils.db_connector import DbConnector


class Db:
    def __init__(self) -> None:
        """ Sets up connection """
        self.connection = DbConnector()
        self.db_connection = self.connection.db_connection
        self.cursor = self.connection.cursor
