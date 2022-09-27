import os
from utils.other import cut_newline


# read lines from trajectories
def read_from_trajectory(path) -> list:
    f = open(path)
    lines = f.readlines()

    stripped_lines = []
    for line in lines[6:]:  # ignore first 6 lines
        stripped_lines.append(cut_newline(line))
    return stripped_lines


# Pretty similar to above, check if this can be done easier
def read_from_labels(path) -> list:
    f = open(path)
    lines = f.readlines()
    stripped_lines = []
    for line in lines:
        stripped_lines.append(cut_newline(line))

    return stripped_lines


# Returns labeled ids as a list.
def get_labeled_ids():
    f = open("dataset\labeled_ids.txt")
    lines = f.readlines()

    labeled_ids = []
    for line in lines:
        labeled_ids.append(cut_newline(line))

    return labeled_ids


# This method retrieves a list of the numbers (folder names) "XXX" which will be used as user ID
def retrieve_list(filter_ids=True) -> list:
    directory_list = list()
    for root, dirs, files in os.walk("./dataset/Data/", topdown=False, followlinks=False):
        for name in dirs:
            try:
                int(name)  # Simple check to see if name is number
                directory_list.append(name)
            except:
                pass

    labeled_ids = get_labeled_ids()
    if filter_ids:
        for label in labeled_ids:
            if label not in directory_list:
                labeled_ids.remove(label)
    return labeled_ids


def get_activity(self, labeled_ids):
    content = []
    for user in labeled_ids:
        path = f"./dataset/Data/{user}/labels.txt"
        content.append((user, self.format_activity(self.read_from_trajectory(path))))
    return content
