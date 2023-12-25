from typing import List, Tuple, Dict, Any
import re
import ast

# update triplets
def add_triplets(G, element, triplets: List[Tuple[str, str, str]]):
    """
    Adds the triplets to the graph
    """
    n_info_triplet_edges = G.nodes[element]['info']['n_info_edges']
    for triplet in triplets:
        start = triplet[0]
        edge = triplet[1]
        end = triplet[2]
        # if the start is the same as the element, then add the edge
        if start == element:
            # if the end node exists, append a uid to the end node
            if G.has_node(end):
                i = 0
                while G.has_node(end+'_'+str(i)):
                    i += 1
                end = end+'_'+str(i)
                # add the node
                print('end->'+end)
                G.add_node(end, name=end, type='info')
            # add the edge
            G.add_edge(start, end, type=edge)
            # increment the number of info edges
            n_info_triplet_edges += 1
            # update the n_info_triplet_edges
            G.nodes[element]['info']['n_info_edges'] = n_info_triplet_edges
    for triplet in triplets:
        start = triplet[0]
        edge = triplet[1]
        end = triplet[2]
        # is the start node exists in the graph as a info node, then add the edge
        # make sure the all noides that follow the reg 'start'+'_'+'number' are also considered
        # element nodes
        ele_nodes = {
            '_'.join(x.split('_')[:-1]):x for x in G.nodes if re.match(start+'_[0-9]+', x)
        }
        if start in ele_nodes.keys():
            # if the start node is of the type info, then add the edge
            if G.nodes[ele_nodes[start]]['type'] == 'info':
                # if the end node doesn't exist, add it
                if G.has_node(end):
                    i = 0
                    while G.has_node(end+'_'+str(i)):
                        i += 1
                    end = end+'_'+str(i)
                    # add the node
                    G.add_node(end, name=end, type='info')
                # add the edge
                G.add_edge(start, end, type=edge)
    return G

def get_unknown_triplets(G, node):
    """
    Generates the triplets for the unknown nodes
    """
    # get the edges if the type of the edge is 'UNKNOWN'
    edges = G.edges(data=True)
    end_nodes = []
    triplets = []
    for edge in edges:
        if edge[2]['type'] == 'UNKNOWN':
            triplets.append((edge[0], edge[2]['type'], edge[1]))
            end_nodes.append(edge[1])
    # if end_node has a edge with type 'UNKNOWN', then add the edge
    for end_node in end_nodes:
        edges = G.edges(end_node, data=True)
        for edge in edges:
            if edge[2]['type'] == 'UNKNOWN':
                triplets.append((edge[0], edge[2]['type'], edge[1]))
    return triplets

# remove multiple unknowns
# for edges in G.edges(data=True)
# remove one edge and the end node if the edge type is 'UNKNOWN' and the end node is of the re type 'UNKNOWN_something' and this appears >1 for the same start node
def remove_duplicates(G):
    """
    Removes the duplicate edges
    """
    # remove all nodes that start with 'UNKNOWN_' and point all incoming edges to the 'UNKNOWN' node instead
    # create the 'UNKNOWN' node if it doesn't exist
    if 'UNKNOWN' not in G.nodes():
        G.add_node('UNKNOWN')
    nodes_to_remove = []
    edges_to_remove = []
    for edge in G.edges(data=True):
        if edge[2]['type'] == 'UNKNOWN':
            if edge[1].startswith('UNKNOWN'):
                nodes_to_remove.append(edge[1])
                edges_to_remove.append(edge)
    # remove the edges
    G.remove_edges_from(edges_to_remove)
    # remove the nodes
    G.remove_nodes_from(nodes_to_remove)
    print('Removed {} nodes'.format(len(nodes_to_remove)))

def graph_preprocess(G):
    remove_duplicates(G)
    # we don't want to delete unnecessary edges, like for example, if get_embeddings is being called somewhere, and 
    return G


# def get_imports(G, element):
#     """
#     Returns a list of imports of the element
#     """
    # imports = ''
    # imports_directly = {}
    # imports_from = {}
    # # find the edges related to the element that are of type 'imports_directly' or 'imports_from'
    # edges = G.edges(element, data=True)
    # for edge in edges:
    #     if edge[2]['type'] == 'imports_directly':
    #         # add the node with a value False
    #         imports_directly[edge[1]] = False
    #     elif edge[2]['type'] == 'imports_from':
    #         # add the node with a value False
    #         imports_from[edge[1]] = False
    # for key in imports_directly.keys():
    #     key_node = G.nodes[key]
    #     if key_node['type'] in ['folder', 'directory', 'external_module', 'external_library']:
    #         imports += 'import '+key+'\n'
    #     imports_directly[key] = True
    # for key in imports_directly.keys():
    #     temp = []
    #     if imports_directly[key] == False:
    #         while True:
    #             break_flag = False
    #         # find the key in the imports_from dict that shares an edge with the key
    #             for key_ in imports_from.keys():
    #                 if G.has_edge(key, key_):
    #                     # if the _key node doesn't have any edge with type 'is_a_submodule_of', then add it to the imports
    #                     if not G.has_edge(key, key_, type='is_a_submodule_of'):
    #                         temp.append(key_)
    #                         imports_from[key_] = True
    #                         break_flag = True
    #             if len(temp) == 0:
    #                 break
    #             if break_flag:
    #                 break
    #         # add the key to the imports
    #         imports += 'from '+'.'.join(temp)+' import '+key+'\n'

    return imports