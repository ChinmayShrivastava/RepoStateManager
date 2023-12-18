import click
import os
import shutil
import json
import networkx as nx
import pickle

repo_map = json.load(open('./repo_map.json'))

@click.command()
@click.argument('repo_name')
def initialize_state(repo_name):

    G = nx.Graph()

    # create a root node with the metadata name=root, type=folder
    G.add_node('root', name='root', type='folder')

    repo_id = repo_map[f'{repo_name}']

    # create a folder with the name of repo_id under state folder
    os.makedirs(os.path.join('state', repo_id), exist_ok=True)

    # from flattened folder + repo_map[repo_name] read lines from the path.txt file
    directory_file = os.path.join('data/flattened', repo_id, 'directory.txt')

    with open(directory_file, 'r') as f:
        filenames = f.readlines()

    # for each line in the file, create nodes to map directories, e.g. if line is a/b/c/d.txt, create nodes a, b, c, d.txt and edges a->b->c->d.txt
    for filename in filenames:
        filename = filename.strip()
        filename = filename.split('/')
        filename = [x for x in filename if x != '']
        for i in range(len(filename)):
            # first check if node exists
            if not G.has_node(filename[i]):
                G.add_node(filename[i], name=filename[i], type='folder' if i != len(filename)-1 else 'file')
            # then check if edge exists, set type as dir-to-dir or dir-to-file
            if i != 0 and not G.has_edge(filename[i-1], filename[i]):
                G.add_edge(filename[i-1], filename[i], type='dir-to-dir' if i != len(filename)-1 else 'dir-to-file')
        # add edge from root to first node
        if not G.has_edge('root', filename[0]):
            G.add_edge('root', filename[0], type='root-to-dir')

    # save the graph as a pickle file
    with open(os.path.join('state', repo_id, 'state_0.pkl'), 'wb') as f:
        pickle.dump(G, f)

if __name__ == '__main__':
    initialize_state()