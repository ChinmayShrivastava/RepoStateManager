import sys
sys.path.append("../")
sys.path.append("../../")
from vspace._chromadb import return_collection
from vspace.vsearch import PineconeVectorSearch
from stringsearch.fuzzy import G, StringSearch
from retrievers.graph import *
from retrievers.defaults import *
import json
from llama_index.tools import FunctionTool
from graph.retrieve import traverse_and_collect
import os
from dotenv import load_dotenv
load_dotenv()

with open("../state/running_state.json", "r") as f:
    running_state = json.load(f)
repo_name = running_state["repo_name"]
repo_id = running_state["repo_id"]

with open(f"../state/{repo_id}/meta/dispatch.json", "r") as f:
    dispatch = json.load(f)

# open the state/repoid/meta/schema.json
with open(f"../state/{repo_id}/meta/schema.json", "r") as f:
    schema = json.load(f)

path_ = f"../state/{repo_id}/meta/storage"
explanations = return_collection(path=path_, collection_name="explanations")
explanations.count()
triplets = return_collection(path=path_, collection_name="triplets")
triplets.count()
code = return_collection(path=path_, collection_name="code")
code.count()

stringmatch = StringSearch()

vectorsearch_expl = PineconeVectorSearch(
    index_name=os.environ['INDEX_NAME'],
    collection_name=f"{repo_name}-explanations"
    )
vectorsearch_code = PineconeVectorSearch(
    index_name=os.environ['INDEX_NAME'],
    collection_name=f"{repo_name}-code"
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
    _triplets = traverse_and_collect(G, node_name, node_type)
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

def return_info(
    node_name: str,
    class_name: str = None,
    ):
    """Takes in node_name and returns code associated with it. Class name is required if the node is a method."""
    # try:
    starting_node = stringmatch.search_one(node_name)[0]
    if class_name is not None:
        starting_node = stringmatch.search_one(node_name, 'class-method')[0]
        class_name = stringmatch.search_one(class_name)[0]

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
    # except Exception as e:
    #     print(e)
    #     string_to_return = f"Sorry, I couldn't find any information on {node_name}. Something went wrong."

    return string_to_return

def semantic_node_finder(
        query: str, 
        type: str = None) -> str:
    """Takes in a human language query and returns the top 5 nodes that match the query and the optional type of the node, if requested"""
    results1 = vectorsearch_expl.search(query=query, type=type)
    results2 = vectorsearch_code.search(query=query, type=type)
    # merge the two results and rerank them according to the number of times they appear
    dict_of_counts = {}
    for result in results1:
        if result in dict_of_counts:
            dict_of_counts[result] += 1
        else:
            dict_of_counts[result] = 1
    for result in results2:
        if result[0] in dict_of_counts:
            dict_of_counts[result] += 1
        else:
            dict_of_counts[result] = 1
    results = sorted(dict_of_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    results = [result[0] for result in results]
    string_to_return = (
        'Find the top five nodes that match the query:\n'
        f"Query: {query}\n"
        '-------------------\n'
    )
    for result in results:
        string_to_return += f"node name: {result[0]} type: {result[1]}\n"
    string_to_return += '-------------------\n'
    return string_to_return

_tools = [
    get_node_edges,
    return_info,
    semantic_node_finder,
]
tools = [
    FunctionTool.from_defaults(fn=tool) for tool in _tools
]

if __name__ == "__main__":
    s = return_info('__init__', 'BaseOpenAIAgent')
    print(s)