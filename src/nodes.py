import datetime
import uuid


class Node:
    def __init__(self, name="noname", content="", 
            creation_date=datetime.datetime.now(),
            update_time=datetime.datetime.now(),
            sub_nodes=[]):
        self.ID = uuid.uuid4() 
        self.name = name
        self.content = content
        self.creation_date = creation_date
        self.update_time = update_time
        self.sub_nodes = []


# NOTE: This might get deleted 
class NodeTree:
    def __init__(self, root_node):
        self.root_node = root_node

    def get_node(self, name, tree=None):
        tree = tree if tree != None else self.root_node_list
        for i in tree:
            if i.name == name:
                return i
            if len(i.sub_nodes) > 0:
                return self.get_node(name = name,
                        tree=i.sub_nodes)
        return False
   #NOTE: nodes are unique. However different nodes can have same sub names 
    def new_note(self, name):
        node = self.get_node(name)
        if node is False:
            self.root_node_list.append(self._add_new_nodes(name))
        else:
            raise NameError("This name already exist")
    
    def new_sub_note(self,parent_name, name):
        parent = self.get_node(parent_name)
        if self.get_node(name, parent.sub_nodes) == False:
            return self._add_new_sub_node(parent, name)
        raise NameError("This name already exist")

    def _add_new_nodes(self, name):
        return Node(name=name, sub_nodes=[])
    
    def _add_new_sub_node(self, parent, name):
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

class TreeEditor:
    def __init__(self, root_node):
        self.root_node = root_node

    def create_node(self, name, parent_node):
        if name not in [node.name for node in parent_node.sub_nodes ]:
            node = Node(name=name)
            parent_node.sub_nodes.append(node)
            return node
        raise NameError("This name is already in use")
            
    def edit_node(self, ID, name, content):
        node = self.get_node_by_id(ID, self.root_node)
        node.content = content
        node.name = name
        print(id(node))
        print("id(node)")

        return node

    def delete_node(self, ID):
        node = self.get_node_by_idx(ID, self.root_node)
        node.sub_nodes = filter(lambda x : x.ID !=ID, node.sub_nodes)
        return node
    def get_node_by_id(self,ID, root_node):
        for i in root_node.sub_nodes:
            if i.ID == ID:
                return i
            if i.sub_nodes != None:
                x = self.get_node_by_id(ID, i)
                if x != None:
                    return x
        return None
    
    def get_node_by_idx(self,ID, root_node):
        for i in root_node.sub_nodes:
            if i.ID == ID:
                return i
            if i.sub_nodes != None:
                x = self.get_node_by_id(ID, i)
                if x != None:
                    return i
        return None       

    def list_all(self,node_ls):
        resp = []
        for i in node_ls.sub_nodes:
            if i.sub_nodes == []:
                resp.append((i.content, i.name,[]))
            else:
                resp.append((i.content,i.name, self.list_all(i)))
        return resp

    def search_node(self,name):
        pass 



if __name__ == "__main__":
    n = TreeEditor(Node(name="genesis"))
    n.create_node("test", n.root_node)
    n.create_node("tet", n.root_node)
    ID = n.create_node("tes", n.root_node.sub_nodes[0]).ID
    n.edit_node(ID, "tes", "anan").ID
    n.delete_node(ID)
    #print(id(n.get_node_by_id(ID, n.root_node)))
    print(n.list_all(n.root_node))
    print(n.get_node_by_id(ID,n.root_node).content)




