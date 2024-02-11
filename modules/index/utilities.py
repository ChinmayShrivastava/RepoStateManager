import re
from modules.actions.graph import add_unique_node

# utility functions
def connect_identifier_node_to_table_root(G, identifier_nodeid):
    # find the node ot type table where value starts with identifier node value (ignore case) and add an edge between the two
    for node in G.nodes:
        if G.nodes[node]['type'] == 'table' and G.nodes[node]['value'].lower().startswith(G.nodes[identifier_nodeid]['value'].lower()):
            G.add_edge(identifier_nodeid, node, type="same_as")
    return G

# check if the identifier is a table name
def is_table_name(identifier):
    # check if the identifier is a table name, i.e. starts with table x or Table x
    if re.match(r"table \d+", identifier, re.IGNORECASE):
        return True
    else:
        return False
    
def parse_tuple_string(s):
    # Remove parentheses and split by comma
    parts = s.strip('()').split(',')
    # Parse each part as a float or a string
    result = []
    for part in parts:
        part = part.strip()
        result.append(part)
    return tuple(result)

def parse_tuple_list_string(s):
    # Remove square brackets and split by parenthesis
    parts = re.findall(r'\(.*?\)', s.strip('[]'))
    # Parse each part as a tuple
    result = [parse_tuple_string(part) for part in parts]
    return result

def add_unique_identifier_node(G, node_type, node_value):
    # check if a node of type identifier with the same value exists
    for node in G.nodes:
        if G.nodes[node]['type'] == node_type and G.nodes[node]['value'] == node_value:
            return G, node
    # if it does not exist, add it
    G, nodeid = add_unique_node(G, node_type, node_value)
    return G, nodeid