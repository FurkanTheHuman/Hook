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
        node.update_time=datetime.datetime.now() 

        return node

    def delete_node(self, ID):
        node = self.get_node_by_idx(ID, self.root_node)
        node2 = self.get_node_by_id(ID, self.root_node)
        node.sub_nodes = [ i  for i in node.sub_nodes if i.ID != ID ]
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
                return root_node
            if i.sub_nodes != None:
                x = self.get_node_by_idx(ID, i)
                if x != None:
                    return i
        return None       

    def list_all(self,node_ls):
        resp = []
        for i in node_ls.sub_nodes:
            if i.sub_nodes == []:
                resp.append((i,[]))
            else:
                resp.append((i, self.list_all(i)))
        return resp

    def search_node(self,name):
        pass 
    def new_note(self, name):
        return Node(name=name)


if __name__ == "__main__":
    # FOR TEST REASONS
    n = TreeEditor(Node(name="genesis"))
    n.create_node("test", n.root_node)
    n.create_node("tet", n.root_node)
    ID = n.create_node("tes", n.root_node.sub_nodes[0]).ID
    n.edit_node(ID, "tes", "anan").ID
    n.delete_node(ID)
    #print(id(n.get_node_by_id(ID, n.root_node)))
    print(n.list_all(n.root_node))
    print(n.get_node_by_id(ID,n.root_node).content)





