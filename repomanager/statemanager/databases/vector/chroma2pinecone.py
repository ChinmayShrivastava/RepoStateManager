import os
import pinecone
from dotenv import load_dotenv
load_dotenv()
from vspace._chromadb import get_embeddings
from agents.retrievers.graph import get_code
from agents.retrievers.defaults import ELEMENTS_THAT_CONTAIN_CODE
import logging
import tqdm

logging.basicConfig(level=logging.INFO)

pinecone.init(      
	api_key=os.environ['PINECONE_API_KEY'], 
	environment=os.environ['PINECONE_ENVIRONMENT']    
)      
index = pinecone.Index(os.environ['INDEX_NAME'])

def _upsert(embeddings, ids, metadatas, namespace, n=50):
    # upsert in batches of n
    vectors = [
        {
            'id': ids[idx],
            'values': embeddings[idx],
            'metadata': metadatas[idx]
        } for idx in range(len(ids))
    ]
    for idx in range(0, len(vectors), n):
        index.upsert(vectors[idx:idx+n], namespace=namespace)
        logging.info(f'Upserted {idx+n} vectors to namespace {namespace}')

def pre_process_text_for_vector_space(text):
    text = text.replace('\n', ' ')
    text = text.replace('\t', ' ')
    text = text.replace('\r', ' ')
    text = text.replace('  ', ' ')
    return text

def migrate(repo_name, repo_id, G, **kwargs):

    if 'explanations' in kwargs:
        explanations = []
        metadatas = []
        ids = []
        for node in tqdm.tqdm(G.nodes(data=True)):
            if 'explanation' in node[1]:
                explanations.append(node[1]['explanation'])
                metadatas.append({
                    'name': node[0],
                    'type': node[1]['type'],
                    'explanation': node[1]['explanation'],
                    'filename': node[1]['elementname'] if node[1]['type'] in ELEMENTS_THAT_CONTAIN_CODE else 'null',
                    # add code if it exists
                    'code': get_code(node[1], repo_id, node[1]['elementname']) if node[1]['type'] in ELEMENTS_THAT_CONTAIN_CODE else 'null',
                })
                ids.append(node[0])
        logging.info(f'Found {len(explanations)} explanations for {repo_name}')
        embeddings = get_embeddings(explanations)
        logging.info(f'Created embeddings for {repo_name}')
        # vectors = [
        #     {
        #         'id': ids[idx],
        #         'values': embeddings[idx],
        #         'metadata': metadatas[idx]
        #     } for idx in range(len(ids))
        # ]
        # index.upsert(vectors, namespace=f'{repo_name}-explanations')
        _upsert(embeddings, ids, metadatas, namespace=f'{repo_name}-explanations')
        logging.info(f'Created vector space for explanations for {repo_name}')

    if 'code' in kwargs:
        codes = []
        metadatas = []
        ids = []
        for node in tqdm.tqdm(G.nodes(data=True)):
            if 'elementname' not in node[1] or 'type' not in node[1]:
                continue
            if node[1]['type'] not in ELEMENTS_THAT_CONTAIN_CODE:
                continue
            codes.append(get_code(node[1], repo_id, node[1]['elementname']))
            metadatas.append({
                'name': node[0],
                'type': node[1]['type'],
                'code': codes[-1],
                'filename': node[1]['elementname'],
                # add explanation if it exists
                'explanation': node[1]['explanation'] if 'explanation' in node[1] else 'null',
            })
            ids.append(node[0])
        logging.info(f'Found {len(codes)} code snippets for {repo_name}')
        embeddings = get_embeddings(codes)
        logging.info(f'Created embeddings for {repo_name}')
        # vectors = [
        #     {
        #         'id': ids[idx],
        #         'values': embeddings[idx],
        #         'metadata': metadatas[idx]
        #     } for idx in range(len(ids))
        # ]
        # index.upsert(vectors, namespace=f'{repo_name}-code')
        _upsert(embeddings, ids, metadatas, namespace=f'{repo_name}-code')
        logging.info(f'Created vector space for code for {repo_name}')