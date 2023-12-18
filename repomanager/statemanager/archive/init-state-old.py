import click
import os
import shutil
import json
import networkx as nx

repo_map = json.load(open('./repo_map.json'))

@click.command()
@click.argument('repo_name')
def initialize_state(repo_name):

    G = nx.Graph()

    repo_id = repo_map[f'{repo_name}']

    # create a folder with the name of repo_id under state folder
    os.makedirs(os.path.join('state', repo_id), exist_ok=True)

    # from flattened folder + repo_map[repo_name] read lines from the path.txt file
    path_file = os.path.join('data/flattened', repo_id, 'path.txt')
    print(path_file)

    with open(path_file, 'r') as f:
        filenames = f.readlines()

    print(filenames)

    # create a root node with the metadata name=root, type=folder
    G.add_node('root', name='root', type='folder')

    for filename in filenames:

        print(filename)

        # replace / with _ and remove \n
        filename = filename.replace('/', '_').strip()

        # read the file
        with open(os.path.join('data/flattened', repo_map[f'{repo_name}'], 'files', filename), 'r') as f:
            content = f.readlines()

        for line in content:
            if line.startswith('import'):
                # split the line by space
                line = line.split(' ')
                # get the second element
                line = line[1]
                # get the first element of the split by .
                line = line.split('.')
                # get the first element
                line = line[0]
                # add an edge from root to the first element of the split by .
                G.add_edge('root', line)

if __name__ == '__main__':
    initialize_state()