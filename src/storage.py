import os
import pickle
from datetime import datetime

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
    def get_name(self):
        raise NotImplementedError("You should implement load method for this class")


    
#PROBLEM: This thing is broken
# fix
class OpenFileStorage(BaseStorage):
    def __init__(self):
        self.node_names = [] 
        self.tree = None
        self.data_dir = os.environ.get("HOME") + "/Desktop/btodo/src"
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


    # implement
    # NOTE: when one of the Storage managers loads the file 
    # they should share it
    # and when I use one file manager and after activate
    # another one they should syncronize 
    # TODO: when writing file I don't save all info on Node()
    def load(self, path="/"):
        this_node = self.load_this_node(path)



class PickleStorage(BaseStorage):
    def __init__(self):
        self._stroage_type = "pickle"
        self.data_dir = os.environ.get("HOME") + "/Desktop/btodo/src"
        self.data_file_name = "tree.P"  
        self.data_path = self.data_dir + self.data_file_name
        if not os.path.exists(os.path.dirname(self.data_dir)):
            try:
                os.makedirs(os.path.dirname(self.data_dir))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
    def get_name(self):
        return self._stroage_type

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

    def _is_name_used(self, name, parent_node):
        if parent_node:
            return name in [node.name for node in parent_node.sub_nodes]
        return None

    def create(self, parent, name):
        if not self._is_name_used(name, parent):
            node = Node(name=name)
            parent.sub_nodes.append(node)
            node.sub_nodes = []
            return node
        raise NameError("This name is already in use "+ name)

    def find_parent(self, child):
        visited = set()
        def depth_first_search(visited, root, child):
            parent = None
            if root not in visited:
                if child.ID in [i.ID for i in root.sub_nodes]:
                    return root
                visited.add(root)
                for sub in root.sub_nodes:
                    test =  depth_first_search(visited, sub, child)
                    if test is not None:
                        return test
            return None
        return depth_first_search(visited, self.tree, child)


    def edit_node(self, node, name, content):
        if node.name == name or not self._is_name_used(name, self.find_parent(node)):
            node.content = content
            node.name = name
            node.update_time = datetime.datetime.now()
        return node

    def delete_node(self, node):
        parent = self.find_parent(node)
        parent.sub_nodes = [ i  for i in parent.sub_nodes if i != node ]
        return node

    def relation_table(self):
        visited = set()
        data = []
        def depth_first_search(visited, root):
            parent = None
            if root not in visited:
                visited.add(root)
                data.append({"node": root , "sub_nodes": [i for i in root.sub_nodes]})
                for sub in root.sub_nodes:
                    depth_first_search(visited, sub)
            return None
        depth_first_search(visited, self.tree)
        return data

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
    def __init__(self, *args, default="pickle"):
        self.storage_methods = [i() for i in args]
        self.default_storage_access = default
    def get_storage_by_name(self, name):
        for storage in self.storage_methods:
            if storage.get_name() == name:
                return storage
        return None

    def get_full_object(self):
        return self.get_default_storage().tree
    def get_default_storage(self):
        return self.get_storage_by_name(self.default_storage_access)

    def set_storage(self, name):
        for storage in self.storage_methods:
            if storage.get_name() == name:
                self.default_storage_access = storage
                return storage

    def create(self, parent, name):
        return self.get_default_storage().create(parent, name)

    def edit(self, node, name, content):
        return self.get_default_storage().edit_node(node, name, content)

    def delete(self, node):
        return self.get_default_storage().delete_node(node)
    def find_parent(self, child):
        return self.get_default_storage().find_parent(child)
    def read(self, node):
        return node.contents

    def get_root(self):
        return self.get_default_storage().tree

    def save(self):
        self.get_default_storage()\
            .save(self.get_storage_by_name(self.default_storage_access).tree)
        print("saved!!!!")
    def load(self):
        self.get_storage_by_name(self.default_storage_access).load()

    def relation_table(self):
        return self.get_storage_by_name(self.default_storage_access).relation_table()

if __name__ == "__main__":
    test = PickleStorage()
    test.load()
    for i in test.relation_table():
        print(">>>", i)
    test.create(test.relation_table()[0].get("node"), "furkan")
    p = test.create(test.relation_table()[0].get("node"), "dogu")
    c = test.create(p, "furkan")
    print("AFTER")
    print("AFTER")
    print("AFTER")
    for i in test.relation_table():
        print(">>>", i)

    print(test.find_parent(c))
