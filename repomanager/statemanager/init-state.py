import click
import os
import shutil
import json
import networkx as nx
import pickle
import ast

repo_map = json.load(open('./repo_map.json'))

@click.command()
@click.argument('repo_name')
# take a bool argument called update, if true, then update the state, else create a new state
@click.option('--update', default=False, help='Update the state')
def initialize_state(repo_name, update):

    if not update:

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
    
    else:

        # read the state_0.pkl file
        repo_id = repo_map[f'{repo_name}']

        # if it doesn't exist, echo error
        if not os.path.exists(os.path.join('state', repo_id, 'state_0.pkl')):
            print('Error: state_0.pkl does not exist')
            return
        
        with open(os.path.join('state', repo_id, 'state_0.pkl'), 'rb') as f:
            G = pickle.load(f)

        # go through the state/repo_id/elements folder and read all the files
        elements_folder = os.path.join('state', repo_id, 'elements')
        files = os.listdir(elements_folder)

        # for each file, read the file and update the graph
        for file in files:

            filename = file.split('.')[0]
            eles = filename.split('!!')
            # TODO: make sure that if the file is a directory, then it is accounted for
            og_file_name = eles[0]+'.py'
            ele_type = eles[1]
            ele_index = eles[2]
            ele_name = eles[3]

            # if the og_file_name is not in the graph, echo error
            if not G.has_node(og_file_name):
                print(f'Error: {og_file_name} does not exist in the graph')
                return
            
            # add the element node if it doesn't exist
            if not G.has_node(ele_name):
                G.add_node(ele_name, name=ele_name, type=ele_type, index=ele_index, elementname=file)
            
            # if the node exists, check if the edge exists
            if not G.has_edge(og_file_name, ele_name):
                G.add_edge(og_file_name, ele_name, type=ele_type)

            # open the file and parse the ast
            with open(os.path.join(elements_folder, file), 'r') as source:
                tree = ast.parse(source.read())
                for node_ in ast.walk(tree):
                    if isinstance(node_, ast.Call):
                        try:
                            if not G.has_node(node_.func.id):
                                continue
                            # if the edge doesn't exist, add it
                            if not G.has_edge(ele_name, node_.func.id):
                                G.add_edge(ele_name, node_.func.id, type='function-call')
                        except:
                            continue

        # save the graph as a pickle file
        with open(os.path.join('state', repo_id, 'state_0.pkl'), 'wb') as f:
            pickle.dump(G, f)

        # # print the nodes and edges
        # print(G.nodes())
        # print(G.edges())

if __name__ == '__main__':
    initialize_state()