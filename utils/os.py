import os
from decouple import config


def read_trajectory_data(path) -> list:
    """ Read trajectory data, ignore first 6 lines """
    with open(path) as f:
        return f.readlines()[6:]


def read_rstrip_file(path) -> list:
    """ Right-strip lines and read file content """
    with open(path) as f:
        return list(map(lambda line: line.rstrip("\n"), f.readlines()))


def get_labeled_ids() -> list:
    """ Returns labeled ids as a list, don't control list with directory structure """
    return read_rstrip_file(os.path.join(config("DATASET_ROOT_PATH"), "dataset", "labeled_ids.txt"))


def get_all_users() -> list:
    """ Get all users based on directory names """
    result = []
    for root, dirs, files in os.walk(os.path.join(config("DATASET_ROOT_PATH"), "dataset", "Data"), topdown=False,
                                     followlinks=False):
        for dir_name in dirs:
            if dir_name.isnumeric():
                result.append(dir_name)
    return result


def get_labeled_users() -> list:
    """ Return list of user IDs with labeled activities, based on directory structure """
    labeled_ids = get_labeled_ids()
    all_users = get_all_users()
    # get all label ids that have an associated directory
    return list(filter(lambda labeled_id: labeled_id in all_users, labeled_ids))


def get_activities():
    """
    Get activity data for all users listed in labeled_ids.
    Format: (end_date, start_date, transportation_mode, user_id)
    """
    labeled_ids = get_labeled_ids()
    activity_data = []
    for user in labeled_ids:
        path = os.path.join(config("DATASET_ROOT_PATH"), "dataset", "Data", user, "labels.txt")
        # Format activity entries into a list
        activity_data += tuple(map(lambda line: tuple(line.split("\t") + [user]), read_rstrip_file(path)[1:]))
    return activity_data
