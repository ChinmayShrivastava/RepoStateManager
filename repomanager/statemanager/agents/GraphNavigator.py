import sys
sys.path.append("../")
from agents import *
from vspace.vsearch import VectorSearch
from typing import List
from langchain.agents import tool
from prompts.general import GRAPH_AGENT_DESCRIPTION_TEMPLATE
from stringsearch.fuzzy import G
from langchain_core.tools import StructuredTool
# import baseclass from pydantic
from pydantic import BaseModel

memory = []

def get_successors(
        node_name: str) -> List[tuple]:
    """Returns a list of tuples of the form (edge_type, node_name)"""
    successors = []
    for edge in G.edges(node_name, data=True):
        if edge[0] == node_name:
            successors.append((edge[2]['type'], edge[1]))
    return successors

def get_predecessors(
        node_name: str) -> List[tuple]:
    """Returns a list of tuples of the form (node_name, edge_type)"""
    predecessors = []
    for edge in G.edges(node_name, data=True):
        if edge[1] == node_name:
            predecessors.append((edge[0], edge[2]['type']))
    return predecessors

def get_memory_context(memory) -> str:
    """Returns a string of lists of triplets of the form 'predecessor_node_name -> edge_type -> node_name'"""
    _string = (
        f'The following are the nodes in memory and therefore don\'t need to be added again:\n'
        f"----------------------------------------\n"
    )
    if len(memory) == 0:
        _string += f'No nodes in memory yet.\n'
    for node in memory:
        _string += f'{node}\n'
    _string += f"----------------------------------------\n"
    return _string

@tool
def get_successor_context(
        node_name: str,
        edge_name: str
        ) -> str:
    """Takes in a node name and the edge type that it has. Returns a string of lists of successor triplets of the form 'node_name -> edge_type -> successor_node_name'"""
    # update the memory
    memory.append(node_name)
    successors = get_successors(node_name)
    _string = (
        f'The following are the successors of the node {node_name}:\n'
        f"----------------------------------------\n"
    )
    for successor in successors:
        if successor[0] == edge_name:
            _string += f'{node_name} -> {successor[0]} -> {successor[1]}\n'
    _string += f"----------------------------------------\n"
    _string = get_memory_context(memory) + _string
    return _string

@tool
def get_predecessor_context(
        node_name: str,
        edge_name: str
        ) -> str:
    """Takes in a node name and the edge type that it has. Returns a string of lists of predecessor triplets of the form 'predecessor_node_name -> edge_type -> node_name'"""
    # update the memory
    memory.append(node_name)
    predecessors = get_predecessors(node_name)
    _string = (
        f'The following are the predecessors of the node {node_name}:\n'
        f"----------------------------------------\n"
    )
    for predecessor in predecessors:
        if predecessor[1] == edge_name:
            _string += f'{predecessor[0]} -> {predecessor[1]} -> {node_name}\n'
    _string += f"----------------------------------------\n"
    _string = get_memory_context(memory) + _string
    return _string

@tool
def get_relevant_connecting_edge_types(
        node_name: str
) -> str:
    """Takes in a node name and returns the type of edges that connect the node to its neighbors"""
    # update the memory
    memory.append(node_name)
    predecessors = get_predecessors(node_name)
    successors = get_successors(node_name)
    _string = (
        f'The following are the connecting edge types of the node \`{node_name}\`:\n'
        f"----------------------------------------\n"
    )
    _string += f'Predecessors are connected by the following edge types:\n'
    for predecessor in predecessors:
        _string += f'{predecessor[1]}\n'
    _string += f"----------------------------------------\n"
    _string += f'Successors are connected by the following edge types:\n'
    for successor in successors:
        _string += f'{successor[0]}\n'
    _string += f"----------------------------------------\n"
    _string = get_memory_context(memory) + _string
    return _string

class GraphNavigatorAgent(LangchainAgent):

    def __init__(self, query, G=G, vector_collection_name='explanations', verbose=True) -> None:
        super().__init__(description=GRAPH_AGENT_DESCRIPTION_TEMPLATE.format(query=query), verbose=verbose)
        self.description = GRAPH_AGENT_DESCRIPTION_TEMPLATE.format(query=query)
        self.verbose = verbose
        self.llm = get_langchain_llm(model='gpt-4')
        self.tools = []
        self.prompt_template = get_prompt_template(self.description)
        self.llm_with_tools = add_tools(self.llm, self.tools)
        self.agent = get_agent(self.llm_with_tools, self.prompt_template)
        self.agent_executor = get_agent_executor(self.agent, self.tools, verbose=verbose)
        self.chat = []
        self.vector_store = VectorSearch(collection_name=vector_collection_name)
        self.query = query
    
    def get_relevant_contex(
            self
    ) -> List[tuple]:
        """Takes in a query and returns the relevant context from the graphstore."""

        # add tools
        self.add_tools([
            get_successor_context,
            get_predecessor_context,
            get_relevant_connecting_edge_types
        ])
        
        # get a initial node to start the search from vector store
        r = self.vector_store.search(query=self.query)[:3]

        _string = (
            f'The following are the nodes to start the graph navigation:\n'
            f"----------------------------------------\n"
        )
        for name, type in r:
            _string += f'Node name: {name}, type: {type}\n'
        _string += f"----------------------------------------\n"
        _string = get_memory_context(memory) + _string
        self._invoke(_string)
        return
    
if __name__ == "__main__":
    query = 'List all the tools that inherit from teh base class of PDF reader'
    _g = GraphNavigatorAgent(query=query)
    _g.get_relevant_contex()
    print(memory)