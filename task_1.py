import utils
import utils.queries as queries
from classes import Db


def insert_users(db):
    """ Inserts users based on directory structure """
    all_users = utils.os.get_all_users()
    labeled_users = utils.os.get_labeled_ids()
    users_to_insert = list(map(lambda usr: (usr, usr in labeled_users), all_users))
    utils.db.insert_rows(db,
                         queries.INSERT_USER,
                         users_to_insert,
                         f"Inserting {len(users_to_insert)} users")


def insert_activities(db):
    """ Inserts activities from list """
    activities_to_insert = utils.os.get_activities()
    utils.db.insert_rows(db, queries.INSERT_ACTIVITY, activities_to_insert,
                         f"Inserting {len(activities_to_insert)} activities")


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
    insert_activities(db)
    cleanup(db)


if __name__ == '__main__':
    main()
