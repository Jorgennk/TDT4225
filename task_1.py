import utils
from classes import Db


def insert_users(db, list_of_users: list):
    """ Inserts users from list """
    labeled_users = db.retrieve_list()
    to_be_inserted = []
    for user in list_of_users:
        to_be_inserted.append((user, user in labeled_users))
    utils.db.insert_rows(db, utils.queries.INSERT_USER, to_be_inserted)


def insert_activities(db, names: list, user_id: int):
    """ Inserts activities from list """
    to_be_inserted = []
    for name in names:
        to_be_inserted.append((user_id, name))
    utils.db.insert_rows(db, utils.queries.INSERT_ACTIVITY, to_be_inserted)


def cleanup(db: Db):
    db.db_connection.close()


def main():
    db = Db()
    print("Task 1")
    cleanup(db)


if __name__ == '__main__':
    main()
