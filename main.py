import pickle
from nodes import NodeTree


class Storage:
    def __init__(self,tree):
        self.tree = tree
        
    def serialize(self, tree):
        return pickle.dumps(tree)
    
    def deserialize(self,f):
        return pickle.loads(f)
    
    def save(self):
        self.DB = self.serialize(self.tree)
    def load(self):
        self.tree = self.deserialize(self.DB)
        return self.tree

# TESTINS CODE
n = NodeTree()

print(n.load_all_notes())

print("----")

n.root_node_list = [
        n.add_new_sub_node(n.add_new_nodes("new"), "sub"),
        n.add_new_nodes("new2")
        ]




print(n)

s = Storage(n)
s.save()
print(s.DB)





