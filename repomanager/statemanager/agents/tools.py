from langchain.agents import tool
import json
import sys
sys.path.append("../")
from vspace._chromadb import return_collection
from vspace.vsearch import VectorSearch
from stringsearch.fuzzy import StringSearch, G
from retrievers.graph import *
from retrievers.defaults import *

with open("state/running_state.json", "r") as f:
    running_state = json.load(f)
repo_id = running_state["repo_id"]

with open(f"state/{repo_id}/meta/dispatch.json", "r") as f:
    dispatch = json.load(f)

# open the state/repoid/meta/schema.json
with open(f"state/{repo_id}/meta/schema.json", "r") as f:
    schema = json.load(f)

path_ = f"state/{repo_id}/meta/storage"
explanations = return_collection(path=path_, collection_name="explanations")
explanations.count()
triplets = return_collection(path=path_, collection_name="triplets")
triplets.count()
code = return_collection(path=path_, collection_name="code")
code.count()

stringmatch = StringSearch.init_from_networkx(G)

vectorsearch = VectorSearch(collection_name="explanations")

# @tool
# def get_schema():
#     """Returns the schema of network graph describing the edge types and the nodes they connect."""
#     # open the state/repoid/meta/schema.json
#     with open(f"../state/{repo_id}/meta/schema.json", "r") as f:
#         schema = json.load(f)
#     schema_string = '\n'.join([f"{v}" for k, v in schema.items()])
#     add_ = (
#         'The following represent the types of edges in the network graph:\n'
#         'They follow the triplet pattern of: information on the starting node, EDGE_NAME, information on the end node.\n'
#         '-------------------\n'
#         )
#     return add_ + schema_string + '\n-------------------\n'

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
def get_edge_information(edge_name: str):
    """takes in an edge name from the schema of the graph and returns the connected nodes"""
    #edge_name = stringmatch.search_one(edge_name)[0]
    string_to_return = ''
    string_to_return += (
        'The following are the triplets related to the edge found in the network graph:\n'
        f"Edge name: {edge_name}\n"
        '-------------------\n'
    )
    for edge in G.edges(data=True):
        if edge_name == edge[2]['type']:
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
    try:
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
    except Exception as e:
        print(e)
        string_to_return = f"Sorry, I couldn't find any information on {node_name}. Something went wrong."

    return string_to_return

@tool
def semantic_node_finder(
        query: str, 
        type: str = None) -> str:
    """Takes in a 3-5 word human language query and returns the top 5 nodes that match the query and the optional type of the node, if requested"""
    if len(query.split(' ')) > 5:
        return "Please enter a query with 3-5 words."
    results = vectorsearch.search(query=query, type=type)
    string_to_return = (
        'Find the top five nodes that match the query:\n'
        f"Query: {query}\n"
        '-------------------\n'
    )
    for result in results:
        string_to_return += f"node name: {result[0]} type: {result[1]}\n"
    string_to_return += '-------------------\n'
    return string_to_return

@tool
def sub_querier(
        query: str
    ) -> str:
    """Takes in a query and returns the sub queries that will be used to retreive relevant information from a graphstore and a vector store."""
    # TODO: requires dynamic few shot examples
    pass

@tool
def schema_tool(
        node_name: str
    ) -> str:
    """Takes in a node name and returns the information on the schema edges that connect to it, along with some node metadata."""
    # gets the edge types that connect to the node
    to_edges = set()
    from_edges = set()
    for edge in G.edges(data=True):
        if node_name in edge:
            if node_name == edge[0]:
                from_edges.add(edge[2]['type'])
            else:
                to_edges.add(edge[2]['type'])
    string_to_return = (
        'The following are the edge types that connect to the node with start and end info.\n'
        'Use this information to query the graphstore for relevant information.\n'
        f"Node name: {node_name}\n"
        '-------------------\n'
        'To edges:\n'
    )
    for edge in to_edges:
        string_to_return += f"{schema[edge]}\n"
    string_to_return += '-------------------\n'
    string_to_return += 'From edges:\n'
    for edge in from_edges:
        string_to_return += f"{schema[edge]}\n"
    string_to_return += '-------------------\n'
    return string_to_return

@tool
def node_tool(
        node_name: str,
        edge_name: str
    ) -> str:
    """Takes in a node name along with the edge name, and returns information on the node content and the connecting content through the edge_name edges."""
    return f"{node_name}"

tools = [get_node_information, return_info, semantic_node_finder]

if __name__ == "__main__":
    node = 'get embedding'
    print(return_info(node))