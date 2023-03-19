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


def insert_trackpoints(db):
    # We wish to avoid I/O reads as they are very slow
    # To minimize the amount of I/O, we insert track points on a per-user basis
    labeled_users = utils.os.get_labeled_ids()
    for user in labeled_users:
        # get all activities for that user, sorted on start_date
        activities = utils.db.select(db,
                                     query=f"SELECT id, user_id, start_date, end_date FROM {queries.TABLE_NAME_ACTIVITY} WHERE user_id={user} ORDER BY start_date")
        activities_dict = {}
        print(activities[0])
        for activity in activities:
            start_time = str(activity[3])
            end_time = activity[2]
            activity_id = activity[0]
            activities_dict[start_time] = {"end_time": end_time, "activity_id": activity_id}
        # get all track points for that user
        trackpoints = utils.os.get_trackpoints(user, activities_dict)
        utils.db.insert_rows(db, queries.INSERT_TRACKPOINT, trackpoints, f"\tInserting {len(trackpoints)} trackpoints for user {user}")


def cleanup(db: Db):
    db.db_connection.close()


def create_tables(db: Db):
    """ Creates all tables required for this assignment. Order: User, Activity, TrackPoint """
    def m(table_name: str):
        return f"Creating table {table_name}"
    utils.db.execute_query(db, queries.CREATE_TABLE_USER, message=m(queries.TABLE_NAME_USER))
    utils.db.execute_query(db, queries.CREATE_TABLE_ACTIVITY, message=m(queries.TABLE_NAME_ACTIVITY))
    utils.db.execute_query(db, queries.CREATE_TABLE_TRACKPOINT, message=m(queries.TABLE_NAME_TRACKPOINT))

def prune_activities(db: Db):
    """ Removes the activites that have no trackpoints """
    utils.db.execute_query(db, queries.REMOVE_ACTIVITY_WO_TRACKPOINT, message=None)


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
    insert_trackpoints(db)
    prune_activities(db)
    cleanup(db)


if __name__ == '__main__':
    main()
