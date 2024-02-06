import os
import networkx as nx
import pickle
import ast
import json
import logging

def _add_unique_node(G, vocabulary, **kwargs):
    # number of nodes in G
    num_nodes = len(G.nodes())
    # add the node
    G.add_node(num_nodes, **kwargs)
    # add the node to the vocabulary
    vocabulary[num_nodes] = kwargs['name']
    return G, vocabulary, num_nodes

def _graph_vocabulary_to_uid_map(G):
    # create a map from the vocabulary to the uid
    vocab_to_uid = {}
    for node in G.nodes():
        vocab_to_uid[G.nodes[node]['name']] = node
    return vocab_to_uid

def _add_class_inheritance_connections(G, asttree):

    # get the classes, and if they have a parent class, add an edge between them
    classes = [node for node in ast.walk(asttree) if isinstance(node, ast.ClassDef)]

    for _class in classes:
        # if _class has a parent class
        try:
            if len(_class.bases) > 0:
                # if the _class name isn't in the graph, add it
                if _class.name not in G.nodes:
                    G.add_node(_class.name, type='class')
                    logging.info(f'Added node {_class.name}')
                # if the parent class isn't in the graph, add it
                if _class.bases[0].id not in G.nodes:
                    G.add_node(_class.bases[0].id, type='class')
                    logging.info(f'Added node {_class.bases[0].id}')
                # add an edge between the two
                G.add_edge(_class.name, _class.bases[0].id, type='parent_class')
                logging.info(f'Added edge {_class.name} -> {_class.bases[0].id}')
        except:
            continue

    return G

def initialize_state(state_loc, tree_map, dir_map):

    num_nodes = 0
    vocabulary = _graph_vocabulary_to_uid_map(G)

    G = nx.DiGraph()

    # create a root node with the metadata name=root, type=folder
    G, vocabulary, nodeid = _add_unique_node(G, vocabulary, name='root', type='folder')

    # load the directory_map from the dir_map file
    with open(dir_map, 'r') as f:
        directorymap = json.load(f)

    # load the tree_map from the tree_map file
    with open(tree_map, 'r') as f:
        treemap = json.load(f)

    # for each line in the file, create nodes to map directories, e.g. if line is a/b/c/d.txt, create nodes a, b, c, d.txt and edges a->b->c->d.txt
    for idx, filename in enumerate(directorymap):
        filename = filename.strip()
        filename = filename.split('/')
        filename = [x for x in filename if x != '']
        for i in range(len(filename)):
            # first check if node exists
            if not G.has_node(filename[i]):
                G, vocabulary, nodeid = _add_unique_node(G, vocabulary, name=filename[i], type='folder' if i != len(filename)-1 else 'file')
            # then check if edge exists, set type as dir-to-dir or dir-to-file
            if i != 0 and not G.has_edge(filename[i-1], filename[i]):
                G.add_edge(vocabulary[filename[i-1]], vocabulary[filename[i]], type='dir-to-dir' if i != len(filename)-1 else 'dir-to-file')
        # add edge from root to first node
        if not G.has_edge('root', filename[0]):
            G.add_edge(vocabulary['root'], vocabulary[filename[0]], type='root-to-dir')

    # save the graph as a pickle file
    with open(state_loc, 'wb') as f:
        pickle.dump(G, f)

    # for each file, read the file and update the graph
    for idx, filename in enumerate(directorymap):

        # filename = file.split('.')[0]
        # eles = filename.split('!!')
        # # TODO: make sure that if the file is a directory, then it is accounted for
        # og_file_name = eles[0].split('@@')[-1]+'.py'
        # ele_type = eles[1]
        # ele_index = eles[2]
        # ele_name = eles[3]

        filename = filename.strip()
        filename = filename.split('/')
        filename = [x for x in filename if x != '']
        filename = filename[-1]

        # if file is not a python file, then skip
        if not filename.endswith('.py'):
            continue

        # if the og_file_name is not in the graph, echo error
        if not G.has_node(vocabulary[filename]):
            logging.error(f'File {filename} not found in the graph.')
            continue

        elementdata = treemap[idx]
        functions = elementdata['functions']
        classes = elementdata['classes']
        elements = functions + classes
        
        for element in elements:

            ele_name = element['name']
            ele_type = element['type']
            file_name = element['file_name']
            code_start_line = element['code_start_line']
            code_end_line = element['code_end_line']
            G, vocabulary, nodeid = _add_unique_node(G, vocabulary, name=ele_name, type=ele_type, filename=file_name, code_start_line=code_start_line, code_end_line=code_end_line)


            G.add_edge(vocabulary[file_name], nodeid, type=ele_type)

            # if element type is class, then load the ast tree
            if ele_type == 'class':
                # open the file and parse the ast
                with open(filename, 'r') as source:
                    codelines = source.readlines()
                    codelines = codelines[code_start_line-1:code_end_line]
                    code = ''.join(codelines)
                try:
                    tree = ast.parse(code)
                except IndentationError:
                    # remove the first four spaces from each line
                    lines = code.split('\n')
                    lines = [line[4:] for line in lines]
                    tree = ast.parse(''.join(lines))
                # name, start_line, end_line
                _classmethods = [(node_.name, node_.lineno, node_.end_lineno) for node_ in ast.walk(tree) if isinstance(node_, ast.FunctionDef)]
                # for each method, add the node and edge
                for method in _classmethods:
                    method_name = method[0]
                    method_start_line = method[1]
                    method_end_line = method[2]
                    G, vocabulary, nodeid = _add_unique_node(G, vocabulary, name=method_name, type='method', filename=filename, code_start_line=method_start_line, code_end_line=method_end_line)
                    
                    G.add_edge(vocabulary[ele_name], nodeid, type='method')
    
    # for each file, read the file and update the graph
    for idx, filename in enumerate(directorymap):

        # filename = file.split('.')[0]
        # eles = filename.split('!!')
        # # TODO: make sure that if the file is a directory, then it is accounted for
        # og_file_name = eles[0].split('@@')[-1]+'.py'
        # ele_type = eles[1]
        # ele_index = eles[2]
        # ele_name = eles[3]

        filename = filename.strip()
        filename = filename.split('/')
        filename = [x for x in filename if x != '']
        filename = filename[-1]

        # if file is not a python file, then skip
        if not filename.endswith('.py'):
            continue

        # if the og_file_name is not in the graph, echo error
        if not G.has_node(vocabulary[filename]):
            logging.error(f'File {filename} not found in the graph.')
            continue

        elementdata = treemap[idx]
        functions = elementdata['functions']
        classes = elementdata['classes']
        elements = functions + classes

        # open the file and parse the ast
        for element in elements:
            ele_name = element['name']
            ele_type = element['type']
            file_name = element['file_name']
            code_start_line = element['code_start_line']
            code_end_line = element['code_end_line']
            # open the file and parse the ast
            with open(filename, 'r') as source:
                codelines = source.readlines()
                codelines = codelines[code_start_line-1:code_end_line]
                code = ''.join(codelines)
            try:
                tree = ast.parse(code)
            except IndentationError:
                # remove the first four spaces from each line
                lines = code.split('\n')
                lines = [line[4:] for line in lines]
                tree = ast.parse(''.join(lines))
            for node_ in ast.walk(tree):
                if isinstance(node_, ast.Call):
                    try:
                        if node_.func.id not in vocabulary:
                            continue
                        # if the edge doesn't exist, add it
                        if not G.has_edge(vocabulary[ele_name], vocabulary[node_.func.id]):
                            # G.add_edge(ele_name, node_.func.id, type='function-call')
                            G.add_edge(vocabulary[ele_name], vocabulary[node_.func.id], type='function-call')
                    except:
                        continue
                # if the instance is a class instance, then add the edge
                if isinstance(node_, ast.Attribute):
                    try:
                        if node_.attr not in vocabulary:
                            continue
                        # if the edge doesn't exist, add it
                        if not G.has_edge(vocabulary[ele_name], vocabulary[node_.attr]):
                            G.add_edge(vocabulary[ele_name], vocabulary[node_.attr], type='class-instance')
                    except:
                        continue
            G = _add_class_inheritance_connections(G, tree)

        # save the graph as a pickle file
        with open(state_loc, 'wb') as f:
            pickle.dump(G, f)