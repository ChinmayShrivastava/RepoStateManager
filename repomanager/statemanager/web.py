import click
import os
import json
import pickle
import logging
from llms.completion import get_llm
from standard.check import is_local
from standard.extract import directory_code_iterator, element_file_iterator, get_element_code
from graph.actions import graph_preprocess
from spiderman.connections import _add_import_connections, _add_class_inheritance_connections
from defaults.trackers import DEFAULT_CONNECTIONS_TRACKER

logging.basicConfig(level=logging.INFO)

repo_map = json.load(open('./repo_map.json'))
llm = get_llm()

@click.command()
@click.argument('repo_name')
def spread_web(repo_name):
    
    repo_id = repo_map[f'{repo_name}']

    # if the file doesn't exist, create it
    if not os.path.exists(f'state/{repo_id}/meta/defaults/connections.json'):
        json.dump(DEFAULT_CONNECTIONS_TRACKER, open(f'state/{repo_id}/meta/defaults/connections.json', 'w'))

    default_tracker = json.load(open(f'state/{repo_id}/meta/defaults/connections.json'))

    codegenerator = directory_code_iterator(repo_id)

    G = pickle.load(open(f'state/{repo_id}/state_0.pkl', 'rb'))
    
    # if not default_tracker["imports"]:

    #     logging.info('Adding import connections')

    #     for code, _filename in codegenerator:

    #         G = _add_import_connections(code, _filename, repo_id, G)
        
    #     pickle.dump(G, open(f'state/{repo_id}/state_0.pkl', 'wb'))

    #     default_tracker["imports"] = True

    #     json.dump(default_tracker, open(f'state/{repo_id}/meta/defaults/connections.json', 'w'))

    # if not default_tracker["graph_preprocess"]:

    #     logging.info('Preprocessing the graph')

    #     # TODO: clear the unknowns from the graph
    #     G = graph_preprocess(G)

    #     pickle.dump(G, open(f'state/{repo_id}/state_0.pkl', 'wb'))

    #     default_tracker["graph_preprocess"] = True

    #     json.dump(default_tracker, open(f'state/{repo_id}/meta/defaults/connections.json', 'w'))

    elements_folder = os.path.join('state', repo_id, 'elements')

    element_dict = element_file_iterator(elements_folder)

    if not default_tracker["parent_class"]:

        logging.info('Adding parent class connections')

        for file in element_dict.keys():

            _, _, asttree = get_element_code(file, elements_folder)
        
            G = _add_class_inheritance_connections(G, asttree)

        pickle.dump(G, open(f'state/{repo_id}/state_0.pkl', 'wb'))

        default_tracker["parent_class"] = True

        json.dump(default_tracker, open(f'state/{repo_id}/meta/defaults/connections.json', 'w'))

    if not default_tracker["async_methods"]:
        pass

if __name__ == '__main__':
    spread_web()