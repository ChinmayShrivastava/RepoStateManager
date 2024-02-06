import networkx as nx

def add_unique_node(G: nx.Graph, node_type: str, node_value: str, **kwargs) -> nx.Graph:
    """Adds a unique node to a networkx Graph.

    Args:
        G (nx.Graph): The networkx Graph to add the node to.
        node_uid (int): The unique identifier for the node.
        node_type (str): The type of node.
        node_value (str, optional): The value of the node. Defaults to None.

    Returns:
        nx.Graph: The networkx Graph with the node added.
        int: The unique identifier of the node.
    """
    node_uid = len(G.nodes)
    if node_uid not in G.nodes:
        G.add_node(node_uid, type=node_type, value=node_value, **kwargs)
    return G, node_uid

def get_nodeid_from_nodevalue(G: nx.Graph, node_value: str) -> int:
    """Gets the node identifier from a node value.

    Args:
        G (nx.Graph): The networkx Graph to search.
        node_value (str): The value of the node to search for.

    Returns:
        int: The unique identifier of the node.
    """
    for nodeid in G.nodes:
        if G.nodes[nodeid]["value"] == node_value:
            return nodeid
    return None