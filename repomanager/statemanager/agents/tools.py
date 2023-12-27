from langchain.agents import tool
import json
import sys
sys.path.append("../")
from vspace._chromadb import return_collection
from stringsearch.fuzzy import StringSearch, G
from retrievers.graph import *
from retrievers.defaults import *

with open("../state/running_state.json", "r") as f:
    running_state = json.load(f)
repo_id = running_state["repo_id"]

with open(f"../state/{repo_id}/meta/dispatch.json", "r") as f:
    dispatch = json.load(f)

path_ = f"../state/{repo_id}/meta/storage"
explanations = return_collection(path=path_, collection_name="explanations")
explanations.count()
triplets = return_collection(path=path_, collection_name="triplets")
triplets.count()
code = return_collection(path=path_, collection_name="code")
code.count()

stringmatch = StringSearch()

@tool
def get_schema():
    """Returns the schema of network graph"""
    # open the state/repoid/meta/schema.json
    with open(f"../state/{repo_id}/meta/schema.json", "r") as f:
        schema = json.load(f)
    schema_string = '\n'.join([f"{v}" for k, v in schema.items()])
    add_ = (
        'The following represent the types of edges in the network graph:\n'
        'They follow the triplet pattern of: information on the starting node, EDGE_NAME, information on the end node.\n'
        '-------------------\n'
        )
    return add_ + schema_string + '\n-------------------\n'

@tool
def get_node_information(node_name: str):
    """takes in a node name representing file, function, imports, etc in the graph and returns the node information"""
    node_name = stringmatch.search_one(node_name)[0]
    string_to_return = ''
    string_to_return += (
        'The following are the triplets related to the node found in the network graph:\n'
        f"Node name: {node_name}\n"
        '-------------------\n'
    )
    for edge in G.edges(data=True):
        if node_name in edge:
            edge0 = edge[0].split('_')
            if edge0[-1].isdigit():
                edge0 = '_'.join(edge0[:-1])
            else:
                edge0 = edge[0]
            edge1 = edge[1].split('_')
            if edge1[-1].isdigit():
                edge1 = '_'.join(edge1[:-1])
            else:
                edge1 = edge[1]
            string_to_return += f"({edge0}, {edge[2]['type']}, {edge1})\n"
    return string_to_return + '-------------------\n'

@tool
def return_info(
    node_name: str,
    class_name: str = None,
    ):
    """Takes in one node and returns all relevant connecting information related to it like code, explanation, etc. Send the class name if the node is a method."""
    starting_node = stringmatch.search_one(node_name)[0]

    snode = G.nodes(data=True)[starting_node]
    snodetype = snode['type']
    elementname = snode['elementname'] if snodetype in ELEMENTS_THAT_CONTAIN_CODE else None

    if elementname is None:
        elementname = G.nodes(data=True)[class_name]['elementname']

    if snodetype not in CODE_TYPES:
        return f"Sorry, I can only return information on {','.join(CODE_TYPES)}. This is a {snodetype}. Try again with a file."

    to_dispatch = dispatch[snodetype]

    if to_dispatch['getCode']:
        # # read the state/repo_id/elements/elementname file into _code
        # with open(f"../state/{repo_id}/elements/{elementname}", "r") as f:
        #     _code = f.read()
        _code = get_code(snode, repo_id, elementname)

    # if to_dispatch['getExplanation']:
    #     # get the explanation
    #     explanation = snode['explanation']
            
    dir_path = elementname.split('!!')[0].replace('@@', '/')+'.py'

    # _append = get_node_information(starting_node)

    string_to_return = ''
    # string_to_return += _append
    # add the code to it, explaining what it is
    string_to_return += (
        'The following is the code related to the node requested in the network graph found in the file represented by the path:\n'
        'Path: ' + dir_path + '\n'
        '-------------------\n'
    )
    string_to_return += f"{_code}\n"
    string_to_return += '-------------------\n'

    return string_to_return
        
tools = [get_node_information, return_info]

if __name__ == "__main__":
    node = 'get embedding'
    print(return_info(node))