import os
import pickle
from nodes import *


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


"""
Storage works three times 
* when program starts
* when program stops 
* when requested

any time there is a change in a node
tree should be updated imidiately

"""
    
# Stroage unit 
# Might get an interface for other types of storages
class Storage:
    """
    user data is stored at $HOME/.local/share/Hook/tree.P
        
    three types of storage
        * local file
        * github
        * server
    saves files and loads files basically
    """
    def __init__(self):
        self.data_dir = os.environ.get("HOME") + "/.local/share/Hook/"
        self.data_file_name = "tree.P"  
        self.data_path = self.data_dir + self.data_file_name
        if not os.path.exists(os.path.dirname(self.data_dir)):
            try:
                os.makedirs(os.path.dirname(self.data_dir))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

    def save(self,tree):
        with open(self.data_path, "wb") as f:
            try:
                pickle.dump(tree, f)
                return True
            except Exception as e:
                print("Cannot write!!!")
                print(e)
                return False
        
        
    def load(self):
        try:
            with open(self.data_path, "rb") as f:
                self.tree = pickle.load(f)
        except EOFError:
            self.tree = Node(name="genesis")
        except FileNotFoundError or EOFError:
            self.tree = Node(name="genesis")
        return self.tree

