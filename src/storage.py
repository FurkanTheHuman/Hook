import os
import pickle
from nodes import *
from abc import ABC, abstractmethod
import errno
from pathlib import Path
from functools import wraps

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



class BaseStorage(ABC):
    def save(self, tree):
        raise NotImplementedError("You should implement save method for this class")
    def load(self):
        raise NotImplementedError("You should implement load method for this class")

def test(f):
    def loop(self, tree, path=""):
        f(self, tree, path="")
        self.get_diff()
    return loop
    

    
#PROBLEM: This thing is broken
# fix
class OpenFileStorage(BaseStorage):
    def __init__(self):
        self.node_names = [] 
        self.data_dir = os.environ.get("HOME") + "/.local/share/Hook/file_storage/"
        if not os.path.exists(os.path.dirname(self.data_dir)):
            try:
                os.makedirs(os.path.dirname(self.data_dir))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

    def check_change(self, file, current_contents):
        contents = file.read()
        print(current_contents)
        if current_contents == "":
            return contents == current_contents
        if current_contents.decode() == contents:
            return False
        return True

    def create_dir(self, path, node):
        print(path, "\n::"+ node.name)
        Path(self.data_dir+path).mkdir(parents=True, exist_ok=True)
        change_state = False
        with open(self.data_dir+path+node.name, "r") as f:
            change_state = self.check_change(f, node.content)
                
        with open(self.data_dir+path+node.name, "w") as f:
            if change_state:
                if node.content == "":
                    f.write("+")                
                else:
                    f.write(str(node.content, "utf-8"))

    # There is a problem with delete operation
    def save(self, tree, path=''):
        self.create_dir(path, tree)
        if tree.sub_nodes != []:
            for i in tree.sub_nodes:
                self.save(i, path+ i.name+"/")


    # implementl
    def load(self):
        pass


class PickleStorage(BaseStorage):
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
    def save(self, tree):
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


# Stroage unit 

class Storage:
    """
    user data is stored at $HOME/.local/share/Hook/tree.P
        
    three types of storage
        * local file
        * github
        * server
    saves files and loads files basically
    """
    def __init__(self, *args):
        self.storage_methods = [i() for i in args]

    def save(self,tree):
        for i in self.storage_methods:
            i.save(tree)
        
    def load(self, from_where=None):
        if from_where == None:
            return self.storage_methods[0].load()

        else:
            return from_where.load()
