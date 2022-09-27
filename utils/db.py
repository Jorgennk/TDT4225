from tabulate import tabulate
import utils.queries as queries


def drop_table(db, table_name):
    print(f"Dropping table {table_name}...")
    execute_query(db, f"DROP TABLE {table_name}")


def show_tables(db):
    db.cursor.execute("SHOW TABLES")
    rows = db.cursor.fetchall()
    print(tabulate(rows, headers=db.cursor.column_names))


def select_all(db, table_name):
    """ Select all rows from table, format nicely and print """
    query = "SELECT * FROM %s"
    db.cursor.execute(query % table_name)
    rows = db.cursor.fetchall()
    print("Data from table %s, raw format:" % table_name)
    print(rows)
    # Using tabulate to show the table in a nice way
    print("Data from table %s, tabulated:" % table_name)
    print(tabulate(rows, headers=db.cursor.column_names))
    return rows


def insert_row(db, query: str, payload: tuple):
    """ Insert a single row """
    try:
        db.cursor.execute(query % payload)
        db.db_connection.commit()
    except:
        db.db_connection.rollback()


def insert_rows(db, query:str, payload: list):
    """ Insert multiple rows in batches. Payload must be a list of tuples """
    try:
        db.cursor.executemany(query, payload)
        db.db_connection.commit()
    except:
        db.db_connection.rollback()


def execute_query(db, query:str):
    """ Execute query that requires no payload """
    try:
        db.cursor.execute(query)
        db.db_connection.commit()
    except:
        db.db_connection.rollback()


def insert_users(db, list_of_users: list):
    """ Inserts users from list """
    labeled_users = db.retrieve_list()
    to_be_inserted = []
    for user in list_of_users:
        to_be_inserted.append((user, user in labeled_users))
    insert_rows(db, queries.INSERT_USER, to_be_inserted)


def insert_activities(db, names: list, user_id: int):
    to_be_inserted = []
    for name in names:
        to_be_inserted.append((user_id, name))
    insert_rows(db, queries.INSERT_ACTIVITY, to_be_inserted)
