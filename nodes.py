import datetime


class Node:
    def __init__(self, name="noname", content="", 
            creation_date=datetime.datetime.now(),
            update_time=datetime.datetime.now(),
            sub_nodes=[]):
        self.name = name
        self.content = content
        self.creation_date = creation_date
        self.update_time = update_time
        self.sub_nodes = sub_nodes


# NOTE: split NodeTree and TreeEdit editing 
class NodeTree:
    def __init__(self):
        self.root_node_list = []

    def load_all_notes(self):
        """
        this should be load notes
        now it just loads from memory
        """
        return self.root_node_list

    def add_new_nodes(self, name):
        return Node(name=name, sub_nodes=[])
    
    def add_new_sub_node(self, parent, name):
        node = Node(name=name, sub_nodes=[])
        parent.sub_nodes.append(node)
        return parent
    
    def list_all(self,node_ls):
        resp = []
        for i in node_ls:
            if i.sub_nodes == []:
                resp.append((i.name,None))
            else:
                resp.append((i.name, self.list_all(i.sub_nodes)))
        return resp

    def __str__(self):
        return str(self.list_all(self.root_node_list))

    def write_content(self, node, text):
        node.content = text
        node.update_time =datetime.datetime.now()
        return node
    #Implement delete

