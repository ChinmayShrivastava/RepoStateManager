import click
import os
import json
import pickle
import logging
from llms.completion import get_llm
from prompts.general import PROMPT_TO_GENERATE_SCHEMA # format the triplets
import random
from vspace.chromadb import return_collection
from standard.extract import get_imports_and_g_variables

# create meta for the edge types - schema
# create the vector spaces for different things, code, paths (more like a string search for path), explanations, triplets, etc.

logging.basicConfig(level=logging.INFO)

repo_map = json.load(open('./repo_map.json'))
llm = get_llm()

@click.command()
@click.argument('repo_name')
def retrieval_preprocess(repo_name):

    repo_id = repo_map[f'{repo_name}']

    G = pickle.load(open(f'state/{repo_id}/state_0.pkl', 'rb'))

    edge_types = set([G.edges[edge]['type'] for edge in G.edges])

    schema = {}

    # if the schema already exists, then don't generate it again
    if not os.path.exists(f"state/{repo_id}/meta/schema.json"):
        for edge_type in edge_types:
            schema[edge_type] = []
            # get random top 10 edges of this type
            edges = [edge for edge in G.edges if G.edges[edge]['type'] == edge_type]
            # randomly sample 10 edges if there are more than 10 edges, otherwise take all the edges
            if len(edges) > 10:
                edges = random.sample(edges, 10)
            # make the prompt
            edge_prompt = ""
            for edge in edges:
                edge_prompt += f"{edge[0]} {edge[1]} {edge_type}\n"
            prompt = PROMPT_TO_GENERATE_SCHEMA.format(triplets=edge_prompt)
            # get the schema
            schema[edge_type] = llm.complete(prompt).text
            logging.info(f"Generated schema for {edge_type}")

        # save the schema into a state/repo_id/meta/ folder, if the meta folder doesn't exist, create it
        if not os.path.exists(f"state/{repo_id}/meta/"):
            os.makedirs(f"state/{repo_id}/meta/")
            logging.info(f"Created meta folder for {repo_id}")
        with open(f"state/{repo_id}/meta/schema.json", "w") as f:
            json.dump(schema, f, indent=4)
            logging.info(f"Saved schema for {repo_id}")
    else:
        logging.info(f"Schema already exists for {repo_id}")

    # create vector space for the code explanations
    # make sure to pass in the metadata as the node name and the node type
    explanations = []
    metadata = []
    ids = []
    for node in G.nodes(data=True):
        if 'elementname' in node[1].keys():
            explanations.append(node[1]['explanation'])
            metadata.append({
                'name': node[0],
                'type': node[1]['type'],
            })
            ids.append(node[0])
    # create the storage folder under meta if it doesn't exist
    if not os.path.exists(f"state/{repo_id}/meta/storage"):
        os.makedirs(f"state/{repo_id}/meta/storage")
        logging.info(f"Created storage folder for {repo_id}")
    # create the vector space
    collection = return_collection(path=f"state/{repo_id}/meta/storage", collection_name="explanations")
    # add the nodes
    collection.add(
        documents=explanations,
        metadatas=metadata,
        ids=ids
    )
    logging.info(f"Created vector space for explanations for {repo_id}")

    # create vector space for the code
    code = []
    metadata = []
    ids = []

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

        code_snippet = open(os.path.join(elements_folder, file)).read()

        # file_code = open(os.path.join('data/flattened', repo_id, 'files/', og_file_name)).read()
        global_vars_imports = get_imports_and_g_variables('/'+og_file_name, repo_id)

        code_snippet = global_vars_imports + '\n' + code_snippet

        code.append(code_snippet)
        metadata.append({
            'name': ele_name,
            'type': ele_type,
            'index': ele_index,
            'containedin': og_file_name,
        })
        ids.append(og_file_name+ele_name)

    # create the storage folder under meta if it doesn't exist
    if not os.path.exists(f"state/{repo_id}/meta/storage"):
        os.makedirs(f"state/{repo_id}/meta/storage")
        logging.info(f"Created storage folder for {repo_id}")
    # create the vector space
    collection = return_collection(path=f"state/{repo_id}/meta/storage", collection_name="code")
    # add the nodes
    collection.add(
        documents=code,
        metadatas=metadata,
        ids=ids
    )
    logging.info(f"Created vector space for code for {repo_id}")

    # create vector space for the triplets
    triplets = []
    metadata = []
    ids = []

    # get all the edges
    edges = G.edges(data=True)
    for edge in edges:
        triplets.append(f"{edge[0]} {edge[2]['type']} {edge[1]}")
        metadata.append({
            'startnode': edge[0],
            'endnode': edge[1],
            'type': edge[2]['type'],
        })
        ids.append(f'{edge}')

    # create the storage folder under meta if it doesn't exist
    if not os.path.exists(f"state/{repo_id}/meta/storage"):
        os.makedirs(f"state/{repo_id}/meta/storage")
        logging.info(f"Created storage folder for {repo_id}")
    # create the vector space
    collection = return_collection(path=f"state/{repo_id}/meta/storage", collection_name="triplets")
    # add the nodes
    collection.add(
        documents=triplets,
        metadatas=metadata,
        ids=ids
    )
    logging.info(f"Created vector space for triplets for {repo_id}")

if __name__ == '__main__':
    retrieval_preprocess()