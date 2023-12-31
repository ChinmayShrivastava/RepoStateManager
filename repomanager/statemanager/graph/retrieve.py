from defaults.graph import parsed_info
from pydantic import BaseModel

class ReturnedEdge(BaseModel):
    start_node: str
    end_node: str
    metadata: dict

class ReturnedEdges(BaseModel):
    edges: list[ReturnedEdge]

def traverse_and_collect(G, node, type) -> ReturnedEdges:
    """Traverses the graph and returns the edges associated with the node"""
    edges = []
    # _parsed_info = parsed_info(type)
    # for path in _parsed_info:
        # edges.extend(collect_info_from_path(G, node, type, path))
    if type=="class":
        edges.extend(collect_info_from_class(G, node))
    else:
        # collect all teh edges from the node
        edges.extend(collect_info_from_all_edges(G, node))
    return ReturnedEdges(edges=edges)

def collect_info_from_all_edges(G, node) -> list[ReturnedEdge]:
    """Collects all the edges from the node"""
    edges = []
    for edge in G.edges(node, data=True):
        edges.append(ReturnedEdge(start_node=edge[0], end_node=edge[1], metadata=edge[2]))
    return edges

def collect_info_from_class(G, node, depth=0) -> list[ReturnedEdge]:
    """Collects all the edges from the node"""
    if depth > 1:
        return []
    edges = []
    # add the edges from class to class-method
    for edge in G.edges(node, data=True):
        if 'type' not in edge[2]:
            continue
        if edge[2]['type']=="class-method":
            edges.append(ReturnedEdge(start_node=edge[0], end_node=edge[1], metadata=edge[2]))
        if edge[2]['type']=="parent_class" and depth<=1:
            # add all the class methods from the parent class
            edges.extend(collect_info_from_class(G, edge[1], depth=depth+1))
    return edges