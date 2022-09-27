
class Table:
    def __init__(self, name, create_string) -> None:
        self.name = name
        self.create_string = create_string
        self.content = []

    def set_content(self, new_content) -> None:
        self.content.append(new_content)
