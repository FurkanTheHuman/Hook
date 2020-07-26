import flask
from flask import request, jsonify


import json 
from TreeEditor import TreeEditor

from slugify import slugify  

from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper
from flask_cors import CORS




def crossdomain(origin=None, methods=None, headers=None, max_age=21600,
                attach_to_all=True, automatic_options=True):
    """Decorator function that allows crossdomain requests.
      Courtesy of
      https://blog.skyred.fi/articles/better-crossdomain-snippet-for-flask.html
    """
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    # use str instead of basestring if using Python 3.x
    if headers is not None and not isinstance(headers, list):
        headers = ', '.join(x.upper() for x in headers)
    # use str instead of basestring if using Python 3.x
    if not isinstance(origin, list):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        """ Determines which methods are allowed
        """
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        """The decorator function
        """
        def wrapped_function(*args, **kwargs):
            """Caries out the actual cross domain code
            """
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers
            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            h['Access-Control-Allow-Credentials'] = 'true'
            h['Access-Control-Allow-Headers'] = \
                "Origin, X-Requested-With, Content-Type, Accept, Authorization"
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator


app = flask.Flask(__name__)
app.config["DEBUG"] = True
#CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app, resources={r"/*": {"origins": "*"}})
#CORS(app, resources={r"/*": {"origins": "*"}}, send_wildcard=True)
test = TreeEditor()

def find_parent(root, child):
    visited = set()
    def depth_first_search(visited, root, child):
        if root not in visited:
            if child in root.sub_nodes:
                return (root.name, root.ID)
            visited.add(root)
            for sub in root.sub_nodes:
                depth_first_search(visited, sub, child)
        return None
    return depth_first_search(visited, root, child)


def none_or_name(node):
    if node is None:
        return None
    return node.name

def generate_table():
    ls = [{"name": entry.get("node").name,
        "id":entry.get("node").ID,
        "parent": none_or_name(test.find_parent(entry.get("node"))),
        "content":entry.get("node").content,
        "sub_nodes": [i.name for i in entry.get("sub_nodes")]} for entry in test.relation_table()]
    return ls

ls = generate_table() 

# URGENT: Use ID's to create security. There can be collisions.
def find_node(addr, table):
    for i in table:
        if i.get("node").name == addr[-1]:
            node = i.get("node")
            return {"name": node.name , "content": node.content}


@app.route('/', methods=['GET'])
@crossdomain(origin='*')
def home():
    if "test" in request.args:
        print(request.args["test"])
    return jsonify(ls)


@app.route('/genesis/<path:addr>', methods=['GET'])
@crossdomain(origin='*')
def get_entry(addr):
    full_addr =  addr.split("/")
    print(addr)
    print(find_node(["genesis"]+full_addr, test.relation_table()))
    return jsonify(find_node(["genesis"]+full_addr, test.relation_table()))

def find_nd(ID):
    for i in test.relation_table():
        if str(i.get("node").ID) == ID:
            return i.get("node")
    return False

@app.route('/update/', methods=['POST'])
def add():
    global ls
    print(request.get_json(force=True))
    print(request)
    req = request.get_json(force=True)

    content = req["content"]

    ID = req["ID"]
    node = find_nd(ID)
    test.edit_node(node, node.name, content)
    test.save()
    ls = generate_table()
    return jsonify({"content": content})

app.run()
