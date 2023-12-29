import logging
from standard.extract import get_imports
from standard.check import is_local
import ast

def _add_import_connections(code, _filename, repo_id, G):

    try:
        imports, importfroms = get_imports(code)
    except:
        logging.error(f'Error in getting imports from {_filename}')
        return

    for import_ in imports:
        if is_local(import_, repo_id):
            if import_+'.py' not in G.nodes:
                # log error
                logging.error(f'Node {import_} not found in graph')
                continue
            else:
                # add the edge
                G.add_edge(_filename, import_+'.py', type='imports_directly')
                logging.info(f'Added edge {_filename} -> {import_}.py')
                continue
        else:
            if import_ not in G.nodes:
                # add the node
                G.add_node(import_, type='external_module')
                logging.info(f'Added node {import_}')
                # add the edge
                G.add_edge(_filename, import_, type='imports_directly')
                logging.info(f'Added edge {_filename} -> {import_}')
                continue
            else:
                # add the edge
                G.add_edge(_filename, import_, type='imports_directly')
                logging.info(f'Added edge {_filename} -> {import_}')
                continue

    for importfrom in importfroms:
        # e.g. of importsfrom [(['os'], ['path', 'walk']), (['something'], ['xyz']), (['abc', 'xyz'], ['abc', 'de'])]
        for element in importfrom[1]:
            # if element is a node in the graph and the '.'.join(importfrom[0]) is a local path
            if is_local('.'.join(importfrom[0]), repo_id):
                if element in G.nodes or element+'.py' in G.nodes:
                    # add the edge
                    G.add_edge(_filename, element if element in G.nodes else element+'.py', type='imports_directly')
                    logging.info(f'Added edge {_filename} -> {element}')
                    if importfrom[0][0] in G.nodes or importfrom[0][0]+'.py' in G.nodes:
                        # add edge from _filename to importfrom[0][0] with type imports_from
                        G.add_edge(_filename, importfrom[0][0] if importfrom[0][0] in G.nodes else importfrom[0][0]+'.py', type='imports_from')
                        logging.info(f'Added edge {_filename} -> {importfrom[0][0]}')
                    continue
            else:
                # add node if it doesn't exist
                if element not in G.nodes:
                    G.add_node(element, type='element')
                    logging.info(f'Added node {element}')
                # add the edge
                G.add_edge(_filename, element, type='imports_directly')
                logging.info(f'Added edge {_filename} -> {element}')
                # reverse the order of importfrom[0]
                for importfrom_, index in zip(importfrom[0][::-1], range(len(importfrom[0]))):
                    if index == 0:
                        # if node doesn't exist, add it
                        if importfrom_ not in G.nodes:
                            G.add_node(importfrom_, type='external_module')
                            logging.info(f'Added node {importfrom_}')
                        G.add_edge(_filename, importfrom_, type='imports_from')
                        logging.info(f'Added edge {_filename} -> {importfrom_}')
                    # if the index is not equal to len(importfrom[0])-1, then add a edge between the two nodes
                    if index != len(importfrom[0])-1:
                        if importfrom_ not in G.nodes:
                            G.add_node(importfrom_, type='external_module')
                            logging.info(f'Added node {importfrom_}')
                        G.add_edge(importfrom_, importfrom[0][index+1], type='is_a_submodule_of')
                        logging.info(f'Added edge {importfrom_} -> {importfrom[0][index+1]}')
                    else:
                        if importfrom_ not in G.nodes:
                            G.add_node(importfrom_, type='external_library')
                            logging.info(f'Added node {importfrom_}')
                        G.add_edge(_filename, importfrom_, type='imports_from')
                        logging.info(f'Added edge {importfrom_} -> {_filename}')
                continue

    return G

def _add_class_inheritance_connections(G, asttree):

    # get the classes, and if they have a parent class, add an edge between them
    classes = [node for node in ast.walk(asttree) if isinstance(node, ast.ClassDef)]

    for class_ in classes:
        # if class_ has a parent class
        try:
            if len(class_.bases) > 0:
                # if the class_ name isn't in the graph, add it
                if class_.name not in G.nodes:
                    G.add_node(class_.name, type='class')
                    logging.info(f'Added node {class_.name}')
                # if the parent class isn't in the graph, add it
                if class_.bases[0].id not in G.nodes:
                    G.add_node(class_.bases[0].id, type='class')
                    logging.info(f'Added node {class_.bases[0].id}')
                # add an edge between the two
                G.add_edge(class_.name, class_.bases[0].id, type='parent_class')
                logging.info(f'Added edge {class_.name} -> {class_.bases[0].id}')
        except:
            continue

    return G