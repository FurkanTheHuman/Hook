from storage import Storage, PickleStorage

class TreeEditor:
    def __init__(self):
        self.storage = Storage(PickleStorage, default="pickle")
        self.storage.load()
    def _is_name_collides(self, name, parent_node):
        return name not in [node.name for node in parent_node.sub_nodes]

    def test(self):
        return self.storage.tree.sub_nodes[3]
    def create_node(self, name, parent_node=None):
        if parent_node is None:
            print(self.storage.get_root())
            return self.storage.create(self.storage.get_root(), name)
        return self.storage.create(parent_node, name)

    def edit_node(self, node, name, content):
        return self.storage.edit(node, name, content)

    def delete_node(self, node):
        return self.storage.delete(node)

    def save(self):
        self.storage.save()
        self.storage.load() 
    def find_parent(self, child):
        return self.storage.find_parent(child)
    def get_full_object(self):
        return self.storage.get_full_object()

    def relation_table(self):
        return self.storage.relation_table()


if __name__ == "__main__":
    ed = TreeEditor()
    for i in ed.relation_table():
        print(i.get("node").name)
        print(" "*5,str([node.name for node in  i.get("sub_nodes")]).replace(",","\n"+" "*5))
        if i.get("node").name == "yeni":
            ed.edit_node(i.get("node"),i.get("node").name,"HELLO world ![asddsa](https://picsum.photos/200/300/)")
    for i in ed.relation_table():
        print(">>>", i)
    
    ed.save()
