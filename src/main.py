#!/usr/bin/env python 
from colorama import Fore, Style
import sys 
import tempfile
import os
from subprocess import call


from nodes import TreeEditor , Node
from storage import Storage


# Highly toxic interface
# Must be fixed
class TerminalUI:
    def __init__(self):
        self.args = sys.argv
        self.storage = Storage()
        self.editor = TreeEditor(self.storage.load())
        self.current_node = self.editor.root_node
        print(self.args)
        if len(sys.argv) < 2:
            self.default_response()
            sys.exit()
   
    def default_response(self):
        pass
    def _get_command(self,arg):
        return self.args[1]
    
    def _get_rest(self, args):
        return self.args[1:]
    
    def evalaluate_args(self):
        print("help")
        command = self._get_command(self.args)
        rest = self._get_rest(self.args)
        print(command)
        if command == "create":
            self.new_note("".join(rest))
            print("aman1")
        if command == "list":
            self.list_view()
        if command == "test":
            self.note_pick(self.editor.root_node)
    def list_view(self):
        ls = self.editor.list_all(self.editor.root_node)
        def disp(p, depth=1):
            for i in p:
                print(Fore.RED + str("*"*depth)+" ", i)
                if i[2] != []:
                    disp(i[2], depth=deph+1)
        disp(ls)

    def list_depth_1(self, ls):
        counter = 1
        for i in ls:
            print(Fore.GREEN + str(counter)+": "+ i.name)
            counter +=1 
        print(Style.RESET_ALL)
    def return_depth_1(self,ls):
        counter = 1
        one = []
        for i in ls:
            one.append((counter, i))
        return one

    def note_pick(self, ls):
        if ls.name == "genesis":
            data = self.return_depth_1(self.editor.root_node.sub_nodes)
            self.list_depth_1(self.editor.root_node.sub_nodes)
            choice = input("CHOSE ONE: ")
        else:
            data = self.return_depth_1(ls.sub_nodes)
            self.list_depth_1(ls.sub_nodes)
            self.current_node = ls
            print("current node: ", ls.name)
            choice = input("CHOSE ONE OR PRESS ENTER FOR THIS NOTE: ")
        if data[int(choice)-1][1].sub_nodes == []:
            self.current_node = data[int(choice)-1][1]
            self.open_editor()

        else:
            self.note_pick(data[int(choice)-1][1].sub_nodes)

            
    def open_editor(self):
        EDITOR = os.environ.get('EDITOR','vim') #that easy!
        initial_message = self.current_node.content # if you want to set up the file somehow
        if type(initial_message) == str:
            print(type(initial_message))
            initial_message = initial_message.encode("utf-8")

        with tempfile.NamedTemporaryFile(suffix=".tmp") as tf:
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
        self.storage.tree =self.editor.root_node 
        self.storage.save()


# Example UI



if __name__ == '__main__':
    term = TerminalUI()
    term.evalaluate_args()
    term.save()





