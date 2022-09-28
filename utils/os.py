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
    """ Returns labeled ids as a list """
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


def get_labeled_users(filter_ids=True) -> list:
    """ Return list of user IDs with labeled activities, based on directory structure """
    # FIXME: Why do we even want to return labeled ids without checking if they have an associated dir?
    labeled_ids = get_labeled_ids()
    if not filter_ids:
        return labeled_ids
    all_users = get_all_users()
    # get all label ids that have an associated directory
    return list(filter(lambda labeled_id: labeled_id in all_users, get_labeled_ids()))


def get_activities(labeled_ids):
    """ Get activity data for all users listed in labeled_ids """
    activities = []
    formatted_data = []
    for user in labeled_ids:
        path = os.path.join(config("DATASET_ROOT_PATH"), "dataset", "Data", user, "labels.txt")
        """ Format activity entries into a list """
        for line in read_trajectory_data(path):
            # Split on tabs
            formatted_data.append(line[1].split("\t"))
        activities.append((user, formatted_data))
        formatted_data.clear()
    return activities