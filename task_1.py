import utils
import utils.queries as queries
from classes import Db


def insert_users(db):
    """ Inserts users from list """
    all_users = utils.os.get_all_users()
    labeled_users = utils.os.get_labeled_users(filter_ids=False)
    to_be_inserted = []
    for user in all_users:
        to_be_inserted.append((user, user in labeled_users))
    utils.db.insert_rows(db, queries.INSERT_USER, to_be_inserted, "Inserting users")


def insert_activities(db, names: list, user_id: int):
    """ Inserts activities from list """
    to_be_inserted = []
    for name in names:
        to_be_inserted.append((user_id, name))
    utils.db.insert_rows(db, queries.INSERT_ACTIVITY, to_be_inserted)


def cleanup(db: Db):
    db.db_connection.close()


def create_tables(db: Db):
    """ Creates all tables required for this assignment. Order: User, Activity, TrackPoint """
    def m(table_name: str):
        return f"Creating table {table_name}"
    utils.db.execute_query(db, queries.CREATE_TABLE_USER, message=m(queries.TABLE_NAME_USER))
    utils.db.execute_query(db, queries.CREATE_TABLE_ACTIVITY, message=m(queries.TABLE_NAME_ACTIVITY))
    utils.db.execute_query(db, queries.CREATE_TABLE_TRACKPOINT, message=m(queries.TABLE_NAME_TRACKPOINT))


def clear_db(db):
    """ Drop all tables """
    utils.db.drop_table(db, queries.TABLE_NAME_TRACKPOINT)
    utils.db.drop_table(db, queries.TABLE_NAME_ACTIVITY)
    utils.db.drop_table(db, queries.TABLE_NAME_USER)


def main():
    db = Db()
    clear_db(db)
    create_tables(db)
    insert_users(db)
    cleanup(db)


if __name__ == '__main__':
    main()
