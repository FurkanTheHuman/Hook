from storage import Storage, PickleStorage

class TreeEditor:
    def __init__(self):
        self.storage = Storage(PickleStorage, default="pickle")
        self.storage.load()
    def _is_name_collides(self, name, parent_node):
        return name not in [node.name for node in parent_node.sub_nodes]

    def create_node(self, name, parent_node=None):
        if parent_node is None:
            return self.storage.create(self.storage.get_root(), name)
        return self.storage.create(parent_node, name)

    def edit_node(self, node, name, content):
        return self.storage.edit(node, name, content)

    def delete_node(self, node):
        return self.storage.delete(node)

    def save(self):
        self.storage.save()

    def relation_table(self):
        return self.storage.relation_table()

    def get_node_by_id(self, ID, root_node):
        for i in root_node.sub_nodes:
            if i.ID == ID:
                return i
            if i.sub_nodes is not None:
                x = self.get_node_by_id(ID, i)
                if x is not None:
                    return x
        return None

    def get_node_by_idx(self, ID, root_node):
        for i in root_node.sub_nodes:
            if i.ID == ID:
                return root_node
            if i.sub_nodes is not None:
                x = self.get_node_by_idx(ID, i)
                if x is not None:
                    return i
        return None

    def list_all(self):
        return self.storage.relation_table()


if __name__ == "__main__":
    ed = TreeEditor()
    tt = ed.create_node("Test")
    ed.edit_node(tt, tt.name, "anan team")
    ed.save()