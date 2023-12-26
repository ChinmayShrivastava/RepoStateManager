import click
import os
import json
import pickle
import logging
from llms.completion import get_llm
from standard.check import is_local
from standard.extract import get_imports, get_imports_and_g_variables
from graph.actions import get_unknown_triplets, graph_preprocess

logging.basicConfig(level=logging.INFO)

repo_map = json.load(open('./repo_map.json'))
llm = get_llm()

@click.command()
@click.argument('repo_name')
def spread_web(repo_name):
    
    repo_id = repo_map[f'{repo_name}']

    with open(os.path.join('data/flattened', repo_id, 'directory.txt'), 'r') as f:
        filenames = f.readlines()
        filenames = [x.strip() for x in filenames]

    for filename in filenames:
            
        filename = filename.strip()

        if filename.split('.')[-1] != 'py':
            continue

        _filename = filename.split('/')[-1]

        filepath = os.path.join('data/flattened', repo_id, 'files/', filename.replace('/', '@@'))
        with open(filepath, 'r') as f:
            # read the code
            code = f.read()
            # take the cursor to the beginning of the file
            f.seek(0)
            # read the lines of the file
            codelines = f.readlines()

        try:
            imports, importfroms = get_imports(code)
        except:
            logging.error(f'Error in getting imports from {filename}')
            continue

        G = pickle.load(open(f'state/{repo_id}/state_0.pkl', 'rb'))

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

        # # get the imports and the global variables
        # context = get_imports_and_g_variables(filename, repo_id)

        # TODO: clear the unknowns from the graph
        G = graph_preprocess(G)

        pickle.dump(G, open(f'state/{repo_id}/state_0.pkl', 'wb'))

if __name__ == '__main__':
    spread_web()