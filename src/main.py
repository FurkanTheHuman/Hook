#!/usr/bin/env python3
import argparse
import sys 
import tempfile
import os
from subprocess import call


from nodes import TreeEditor 
from storage import Storage, PickleStorage, OpenFileStorage


# Highly toxic interface
# Must be fixed
"""
Design notes:
    A UI is a connector between Storage and and TreeEditor

NOTE: Write the details of storage and tree interface for UI
by interface I mean which actions should be 

----
there should be a way to pick nodes
there should be a way to edit nodes
there should be a way to delete nodes
there should be a way to see nodes
there should be a way to create nodes

there should be appropriate args


TODO: remove every relation with Node class
    Node()
    sub_nodes
    ...

"""
class TerminalUI:
    def __init__(self):
        self.args = sys.argv
        self.storage = Storage(PickleStorage)
        self.editor = TreeEditor(self.storage.load())
        self.current_node = self.editor.root_node
        self.args = self.set_up_args()
        if len(sys.argv) < 2:
            self.default_response()
            sys.exit()
   
    
    def evalaluate_args(self):
        if self.args.command == "new":
            if self.args.value != None:
                self.new_note(self.args.value)
            else: 
                self.parser.error("new command reqires name for the note")
        if self.args.command == "new_sub":
            if self.args.value != None:
                note = self.note_pick(self.current_node)
                self.current_node.sub_nodes.append(self.editor.new_note(self.args.value))
                self.edit_note(self.current_node.sub_nodes[-1])
            else: 
                self.parser.error("new_sub command reqires name for the note")

        if self.args.command == "edit":
            note = self.note_pick(self.current_node)
            self.edit_note(note)
        if self.args.command == "delete":
            self.list_view()
            print("WARNING You are deleting a note!")
            note = self.note_pick(self.current_node)
            self.editor.delete_node(note.ID)
            print("NOTE HAS BEEN DELETED!")
            self.list_view()
        if self.args.command == "list":
            self.list_view()
        if self.args.command == "chose":
            pass
        if self.args.command == "jump":# problem: a file name can't contain ";" 
            def search(tree_list, node_name):
                for i in tree_list:
                    if i.name ==node_name:
                        return i
                raise NameError("ERR: "+ i + " not found in " + position_on_tree.name)

            addr = self.args.value.split(",")
            position_on_tree= self.current_node
            for i in addr:
                if i not in [node.name for node in self.return_depth_1(position_on_tree.sub_nodes)]:
                    raise NameError("ERR: "+ i + " not found in " + position_on_tree.name)
                else:
                    tmp_node_list = self.return_depth_1(position_on_tree.sub_nodes)
                    position_on_tree = search(position_on_tree.sub_nodes, i)
            self.current_node = position_on_tree
            self.open_editor()

    def list_view(self):
        # Change this.
        ls = self.editor.list_all(self.editor.root_node)
        def disp(p, depth=0):
            for i in p:
                node, sub_nodes = i 
                print(str(" "*depth+ "-")+" " , end="")
                print( node.name , "last edited: [", node.update_time,"]")
                if sub_nodes != []:
                    disp(sub_nodes, depth=depth+len(node.name)+2)
        disp(ls)

    def list_depth_1(self, ls):
        counter = 1
        for i in ls:
            print(str(counter)+": "+ i.name)
            counter +=1 
        print()
    
    def return_depth_1(self,ls):
        one = []
        for i in ls:
            one.append(i)
        return one
    # Maybe there should be a strong check for genesis node
    def note_pick(self, ls):
        print("note_pick")
        data = self.return_depth_1(ls.sub_nodes)
        self.list_depth_1(ls.sub_nodes)
        self.current_node = ls
        if ls.name == "genesis": # ???
            # What happens when there is no node and someone "edit"s??
            choice = input("CHOSE ONE: ")
            return self.note_pick(data[int(choice)-1]) 
        else:
            if ls.sub_nodes == []:
                return self.current_node
            print("current node: ", ls.name)
            choice = input("CHOSE ONE OR PRESS ENTER FOR THIS NOTE: ")
            if choice == "":
                return self.current_node
            else:
                return self.note_pick(data[int(choice)-1]) 
    def edit_note(self, data):
        self.current_node = data
        self.open_editor()

        return data            
    def open_editor(self):
        EDITOR = os.environ.get('EDITOR','vim') #that easy!
        initial_message = self.current_node.content 
        if type(initial_message) == str:
            initial_message = initial_message.encode("utf-8")

        with tempfile.NamedTemporaryFile(suffix=".md") as tf:
            tf.write(initial_message)
            tf.flush()
            call([EDITOR, tf.name])

            # do the parsing with `tf` using regular File operations.
            # for instance:
            tf.seek(0)
            edited_message = tf.read()
            self.editor.edit_node(self.current_node.ID, self.current_node.name, edited_message)

    def new_note(self, name):
        self.current_node = self.editor.create_node(name, self.current_node)
        self.open_editor()
        

    def save(self):
        self.storage.save(self.editor.root_node)

    def set_up_args(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument("command", type=str,
                help="option", choices=["new","new_sub" ,"edit","delete", "list", "choice", "jump"])
        self.parser.add_argument("value", nargs="?",
                default=None, help="value")
        args = self.parser.parse_args()
        return args




# for an interface like browser this code should be a loop.
# after any change evaluate commands and  
if __name__ == '__main__':
    term = TerminalUI()
    term.evalaluate_args()
    term.save()





