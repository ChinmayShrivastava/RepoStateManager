import sys
import os
# navigate to the parent directory, and make it as the current working directory
# os.chdir("../../")
# sys.path.append("./")
# print(os.getcwd())
# print(sys.path)
from vspace._chromadb import return_collection
from vspace.vsearch import PineconeVectorSearch, VectorSearch
from stringsearch.fuzzy import G, StringSearch
from agents.retrievers.graph import *
from agents.retrievers.defaults import *
import json
from llama_index.tools import FunctionTool
from graph._graph import NetworkXGraph, Neo4JGraph
import os
from dotenv import load_dotenv
load_dotenv()
import logging
from vspace.pipelines.general import get_initial_information
from vspace.pipelines.docsearch import get_docs

logging.basicConfig(level=logging.INFO)

with open("state/running_state.json", "r") as f:
    running_state = json.load(f)
repo_name = running_state["repo_name"]
repo_id = running_state["repo_id"]

# with open(f"state/{repo_id}/meta/dispatch.json", "r") as f:
#     dispatch = json.load(f)

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

vectorsearch_expl = PineconeVectorSearch(
    index_name=os.environ['INDEX_NAME'],
    collection_name=f"{repo_name}-explanations"
    )
vectorsearch_code = PineconeVectorSearch(
    index_name=os.environ['INDEX_NAME'],
    collection_name=f"{repo_name}-code"
    )
vectorsearch_docs = PineconeVectorSearch(
    index_name=os.environ['INDEX_NAME'],
    collection_name=f"{repo_name}-docs"
    )

# graph_nx = NetworkXGraph.from_G(
#     repo_id=repo_id,
#     G=G
# )

graph_nx = Neo4JGraph.from_url(
    url=f"{os.getenv('NEO4J_URL')}",
    auth=(os.getenv('NEO4J_ADMIN'), os.getenv('NEO4J_PASSWORD_DROPLET')),
)

def get_node_edges(node_name: str, node_type: str = None):
    """Takes in a node name and an optional node_type (class, class-method, function) in the graph and returns the network graph triplets associated with it"""
    if node_type is not None:
        node_name = stringmatch.search_one(node_name, type=node_type)[0]
    else:
        node_type = 'class'
        node_name = stringmatch.search_one(node_name, type=node_type)[0]
    string_to_return = ''
    string_to_return += (
        'The following are the triplets related to the node found in the network graph:\n'
        f"Node name: {node_name}\n"
        '-------------------\n'
    )
    # _triplets = traverse_and_collect(graph_nx, node_name, node_type)
    _triplets = graph_nx.get_edges_by_type(
        {
            'name': node_name,
            'type': node_type,
        }
    )
    # _triplets are of type ReturnedEdges, where each edge is of type ReturnedEdge, where each edge has a start_node, end_node, and metadata
    edges = [(edge.start_node, edge.end_node, edge.metadata) for edge in _triplets.edges]
    for edge in edges:
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
    string_to_return += '-------------------\n'
    _append = ''
    for edge in edges:
        if node_name not in edge:
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
            _append += f"({edge0}, {edge[2]['type']}, {edge1})\n"
    if _append != '':
        string_to_return += (
            'The following are the triplets related to the parent class of the class=:\n'
            '-------------------\n'
        )
        string_to_return += _append
        string_to_return += '-------------------\n'
    return string_to_return

# old name was `return_info`
def get_code(
    node_name: str,
    ):
    """This tool takes in a node_name representing a class, function or a class_name.method_name and returns the associated code from the knowledge base."""
    
    # initialize the is_method flag
    is_method = False
    # if the node_name is a class.method, split it into class_name and method_name
    if '.' in node_name:
        # split the node_name into class_name and method_name
        class_name, node_name = node_name.split('.')
        # set the is_method flag to True
        is_method = True
    # else, set the class_name to None
    else:
        class_name = None

    if class_name is not None:
        starting_node = stringmatch.search_one(node_name, 'class-method')[0]
        class_name = stringmatch.search_one(class_name)[0]
    else:
        # set the starting node as the closest fuzzy match to the node_name
        starting_node = stringmatch.search_one(node_name)[0]

    snode = graph_nx.get_node_metadata(starting_node)
    snodetype = snode['type']
    elementname = snode['elementname'] if snodetype in ELEMENTS_THAT_CONTAIN_CODE else None

    if elementname is None:
        elementname = graph_nx.get_node_metadata(class_name)['elementname']

    if snodetype not in CODE_TYPES:
        return f"Sorry, I can only return information on {','.join(CODE_TYPES)}. This is a {snodetype}. Try again with a file."

    _code = graph_nx.get_code(snode, elementname)
    
    dir_path = elementname.split('!!')[0].replace('@@', '/')+'.py'

    string_to_return = ''
    if is_method:
        string_to_return += f"The code info for the method {node_name} for the class {class_name} is:\n"
    else:
        string_to_return += f"The code info for the {snode['type']} {node_name} is:\n"
    string_to_return += (
        'The path to the code is:\n'
        'Path: ' + dir_path + '\n'
        '-------------------\n'
        'The code is:\n'
    )
    string_to_return += f"{_code}\n"
    string_to_return += '-------------------\n'

    return string_to_return

def semantic_info_finder(
        query: str) -> str:
    """This tool returns relevant information to the query from the knowledge base."""
    # """Takes in a 3-5 word human language query and returns the top 5 nodes that match the query and the optional type of the node, if requested"""
    if len(query.split(' ')) > 5:
        return "Please enter a query with 3-5 words."
    r = get_initial_information(query, graph_nx, vectorsearch_expl)
    return r

def docs_search(
        query: str
        ) -> str:
    """This tool returns some use cases and insights from the knowledge base based on the query. Use it to search for documentation."""
    docs = get_docs(query, vectorsearch_docs, graph_nx)
    _string = 'The following is some information extracted from the documentation:\n'
    _string += '-------------------\n'
    for doc in docs:
        _string += f"{doc}\n"
        _string += '-------------------\n'
    return _string

def call_knowledge_base_or_not(
    call_knowledge_base_or_not: bool
    ):
    """This tool takes in a boolean call_knowledge_base_or_not and returns the appropriate response. Always call this tool when the user queries something."""
    if call_knowledge_base_or_not:
        return "[KILL]"
    else:
        return "[CONTINUE]"

_tools = [
    docs_search,
    get_node_edges,
    get_code,
    semantic_info_finder,
]

tools = [
    FunctionTool.from_defaults(fn=tool) for tool in _tools
]

_godfather_tools = [
    call_knowledge_base_or_not,
]

godfather_tools = [
    FunctionTool.from_defaults(fn=tool) for tool in _godfather_tools
]

if __name__ == "__main__":

    s = get_code('Openaiagent.from_tools')
    print(s)