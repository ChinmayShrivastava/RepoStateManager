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
    triplets = []
    for edge in edges:
        if edge[2]['type'] == 'UNKNOWN':
            triplets.append((edge[0], edge[2]['type'], edge[1]))
    return triplets

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