import click
import json
import logging
import pickle
from llms.completion import get_llm
from llms.parse import parse_tripets
from standard.extract import directory_file_iterator
from standard.extract import markdown_parser, directory_file_iterator, ipynb_parser
from bs4 import BeautifulSoup
from prompts.general import PROMPT_TO_EXTRACT_INFO_FROM_DOCS
from vspace._chromadb import return_collection, get_embeddings, add_docs_to_collection
import tqdm

logging.basicConfig(level=logging.INFO)

repo_map = json.load(open('./repo_map.json'))
llm = get_llm()

@click.command()
@click.argument('repo_name')
def update_docs(repo_name):

    repo_id = repo_map[f'{repo_name}']

    information = json.load(open(f'state/{repo_id}/meta/defaults/information.json', 'r'))

    G = pickle.load(open(f'state/{repo_id}/state_0.pkl', 'rb'))

    print(G.nodes["OpenAIAgent"])

    files = directory_file_iterator(repo_id=repo_id, get_non_py_files=True)

    logging.info(f'extracted {len(files)} files')

    docs_dispatch = information["docs"]

    if docs_dispatch["graph"] == False:

        for file in tqdm.tqdm(files, total=len(files)):
            if "@@docs@@" not in file:
                continue
            if file.endswith('.ipynb'):
                # get the content of the file
                content = open(file).read()
                # parse the markdown
                parsed = ipynb_parser(content)
                # remove the html tags from each list element
                parsed = [BeautifulSoup(p, features="html.parser").get_text() for p in parsed]
            elif file.endswith('.md'):
                # get the content of the file
                content = open(file).read()
                # parse the markdown
                parsed = markdown_parser(content)
                # remove the html tags from each list element
                parsed = [BeautifulSoup(p, features="html.parser").get_text() for p in parsed]
            else:
                continue
            elementname = file.split('/')[-1]
            pathname = file.split('/')[-1].replace("@@", "/")
            filename = pathname.split('/')[-1]
            # log error if a node names filename.split('/')[-1] doesn't exist which has a type "file"
            if not G.has_node(filename) and G.nodes[filename]['type'] != 'file':
                logging.error(f'Node {filename} of type file does not exist')
                continue
            # if that node has 1 or more edges of type "content-chunk", continue
            if len([e for e in G.edges(filename, data=True) if e[2]['type'] == 'content-chunk']) > 0:
                logging.error(f'Node {filename} of type file already has content-chunk edges')
                continue
            # log in yellow, updating node with name filename.split('/')[-1] and type "file"
            logging.info(f'\033[93mUpdating node with name {filename} and type file\033[0m')
            i = 0
            new_nodes = []
            for p in parsed:
                _data = {
                    "name": f"{filename} - {i}",
                    "flattened_name": elementname,
                    "content": p,
                    "type": "docs",
                    "og_file_name": filename,
                    "og_file_path": pathname,
                    "index": i
                }
                new_nodes.append(_data)
                i += 1
                # add the node to the graph if it doesn't exist
                if not G.has_node(_data['name']):
                    G.add_node(_data['name'], **_data)
                # add the edge from the filename node to the node with name _data['name']
                if not G.has_edge(filename, _data['name']):
                    G.add_edge(filename, _data['name'], type='content-chunk')
            for node in new_nodes:
                _prompt = PROMPT_TO_EXTRACT_INFO_FROM_DOCS.format(snippet=node['content'])
                try:
                    response = llm.complete(_prompt).text
                except Exception as e:
                    logging.error(e)
                    continue
                triplets = response.split('\n')
                parsed_triplets = parse_tripets(triplets)
                # for each triplet, add the edge to the graph
                for triplet in parsed_triplets:
                    G.add_edge(node["name"], triplet[2], type=triplet[1])
                logging.info(f'\033[92m{parsed_triplets}\033[0m')
                # log in blue, updating node with name node['name'] and type "docs"
                logging.info(f'\033[94mUpdated node with name {node["name"]} and type docs\033[0m')
            # save the graph as a pickle file
            with open(f'state/{repo_id}/state_0.pkl', 'wb') as f:
                pickle.dump(G, f)
            
            # updat dispatch
            docs_dispatch["graph"] = True
            information["docs"] = docs_dispatch
            json.dump(information, open('state/{repo_id}/meta/defaults/connections.json', 'w'))

    if docs_dispatch["vector"] == False:

        # get the edges' nodes connected to all the nodes ending with a .ipynb or .md
        _nodes = [e[1] for e in G.edges(data=True) if e[0].endswith('.ipynb') or e[0].endswith('.md')]

        docs = []
        metadatas = []
        ids = []

        for node in tqdm.tqdm(_nodes, total=len(_nodes)):
            # get all the edges' nodes to the node of type USE_CASE or INSIGHT
            _docs = [e[1] for e in G.edges(node, data=True) if e[2]['type'] == 'USE_CASE' or e[2]['type'] == 'INSIGHT']
            _metadata = [
                {
                    "type": e[2]['type'],
                    "node": node
                }
                for e in G.edges(node, data=True) if e[2]['type'] == 'USE_CASE' or e[2]['type'] == 'INSIGHT'
            ]
            _ids = [f"{node} - {i}" for i in range(len(_docs))]
            docs.extend(_docs)
            metadatas.extend(_metadata)
            ids.extend(_ids)

        # create a collection
        collection = return_collection(path=f'state/{repo_id}/meta/storage', collection_name='docs')

        # add the docs to the collection
        collection = add_docs_to_collection(docs, metadatas, ids, collection)

        logging.info(f'Added {len(docs)} docs to the collection')

        # update the dispatch
        docs_dispatch["vector"] = True
        information["docs"] = docs_dispatch
        json.dump(information, open('state/{repo_id}/meta/defaults/information.json', 'w'))

if __name__ == '__main__':
    update_docs()