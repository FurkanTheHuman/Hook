import datetime
import uuid
#   from storage import Storage, PickleStorage


class Node:
    def __init__(self, name="noname", content="",
                 creation_date=datetime.datetime.now(),
                 update_time=datetime.datetime.now(),
                 sub_nodes=[]):
        self.ID = uuid.uuid4()
        self.name = name
        self.content = content
        self.creation_date = creation_date
        self.update_time = update_time
        self.sub_nodes = sub_nodes

