# Basically just puts the different fields in into separated list
# so they are easier to work with
def format_activity(self, list_of_entries) -> list:
    formatted = []
    for line in list_of_entries:
        # Split on tabs
        formatted.append(line[1].split("\t"))

    return formatted


def cut_newline(input_line) -> str:
    return input_line.rstrip("\n")
