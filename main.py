import pickle
from nodes import NodeTree
import os

"""
We have a model that works for now. 
we need to save and retrieve from this model
Approaches: 
    * save pickle object
        > this method simple however there is problems with
        updating. the whole tree needs to be loaded if I change a single letter
        however this is easy to implement and even for real world cases not so slow
        or memory problamatic. Also it is easy to change after implementing it.
    * using db
        > Most performance effective. might migrate to this after pickle
    * using just files
        good for seeing files but easy to corrupt. So this thing only should be used as 
        backup. Combine with db model.
"""


# NOT NECESSARY FOR NOW
#class Config:
#    """
#    base config file.
#    by default it is in $HOME/.config/Hook/conf.ini
#    
#    PARAMS:
#     
#    """
    


class Storage:
    """
    user data is stored at $HOME/.local/share/Hook/tree.P
    config file stored at $HOME/.config/Hook/conf.ini
    NOTE: Why am I using conf??
        
    saves files and loads files basically
    """
    def __init__(self,tree):
        self.tree = tree
        self.data_dir = os.environ.get("HOME") + "/.local/share/Hook/"
        self.data_file_name = "tree.P"  
        self.data_path = self.data_dir + self.data_file_name
        if not os.path.exists(os.path.dirname(self.data_dir)):
            try:
                os.makedirs(os.path.dirname(self.data_dir))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

    def save(self):
        # fuck that func
        def serialize(tree, handle):
            return pickle.dump(tree, handle)
        with open(self.data_path, "wb") as f:
            try:
                serialize(self.tree, f)
                return True
            except Exception as e:
                print("Cannot write!!!")
                print(e)
                return False
        
    def load(self):
        with open(self.data_path, "rb") as f:
            self.tree = pickle.load(f)
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
print(s.load())





