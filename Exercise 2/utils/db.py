from tabulate import tabulate


def drop_table(db, table_name) -> bool:
    """ Drop table. Return True if successful, False otherwise """
    return execute_query(db, f"DROP TABLE {table_name}", f"Dropping table {table_name}...")


def show_tables(db):
    db.cursor.execute("SHOW TABLES")
    rows = db.cursor.fetchall()
    print(tabulate(rows, headers=db.cursor.column_names))


def select(db, query, display_raw=False, display_table=False, table_name="UNDEFINED_TABLE"):
    """ Select all rows from table, format nicely and print """
    db.cursor.execute(query)
    rows = db.cursor.fetchall()
    if display_raw:
        print("Data from table %s, raw format:" % table_name)
        print(rows)
    if display_table:
        # Using tabulate to show the table in a nice way
        print("Data from table %s, tabulated:" % table_name)
        print(tabulate(rows, headers=db.cursor.column_names))
    return rows


def insert_row(db, query: str, payload: tuple, message: str = None) -> bool:
    """ Insert a single row. Return True if successful, False otherwise """
    if message is not None:
        print(message)
    try:
        db.cursor.execute(query % payload)
        db.db_connection.commit()
        print("\t...SUCCESS")
        return True
    except Exception as e:
        print(e)
        db.db_connection.rollback()
        return False


def insert_rows(db, query: str, payload: list, message: str = None) -> bool:
    """
    Insert multiple rows in batches. Payload must be a list of tuples. Return True if successful, False otherwise
    """
    if message is not None:
        print(message)
    try:
        db.cursor.executemany(query, payload)
        db.db_connection.commit()
        print("\t...SUCCESS")
        return True
    except Exception as e:
        print(e)
        db.db_connection.rollback()
        return False


def execute_query(db, query: str, message: str = None, print_success=True) -> bool:
    """ Execute query that requires no payload. Return True if successful, False otherwise """
    if message is not None:
        print(message)
    try:
        db.cursor.execute(query)
        db.db_connection.commit()
        if print_success:
            print("\t...SUCCESS")
        return True
    except Exception as e:
        print(e)
        db.db_connection.rollback()
        return False


def execute_query_get_result(db, query: str, message: str = None, print_success=True):
    """ Execute query that requires no payload. Return True if successful, False otherwise """
    if message is not None:
        print(message)
    try:
        db.cursor.execute(query)
        if print_success:
            print("\t...SUCCESS")
        return db.cursor.fetchall()
    except Exception as e:
        print(e)
        return None
