import logging

def check_graph_elements(G, node1, node2):
    if not G.has_node(node1):
        logging.info('Error: {} does not exist in the graph'.format(node1))
        return False
    if not G.has_node(node2):
        logging.info('Error: {} does not exist in the graph'.format(node2))
        return False
    if not G.has_edge(node1, node2):
        logging.info('Error: edge from {} to {} does not exist in the graph'.format(node1, node2))
        return False
    return True