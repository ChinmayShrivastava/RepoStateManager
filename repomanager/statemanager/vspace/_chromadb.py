import os
from chromadb import PersistentClient, HttpClient
from chromadb.utils import embedding_functions
from dotenv import load_dotenv
load_dotenv()
from langchain.embeddings import OpenAIEmbeddings

_embeddings_model = OpenAIEmbeddings(openai_api_key=os.environ['OPENAI_API_KEY'], disallowed_special=())

def get_embeddings(listoftexts) -> list:
    embeddings = _embeddings_model.embed_documents(listoftexts)
    return embeddings

# TODO: make sure the collection names are unique per repo
def return_collection(path=None, collection_name=None):
    assert path is not None, "Path isn't specified"
    assert collection_name is not None, "Collection name isn't specified"
    chroma_client = PersistentClient(path=path)
    emb_fn = embedding_functions.OpenAIEmbeddingFunction(
        api_key=os.getenv('OPENAI_API_KEY'),
        model_name="text-embedding-ada-002"
    )
    collection = chroma_client.get_or_create_collection(name=collection_name, embedding_function=emb_fn, metadata={"hnsw:space": "cosine"})
    return collection

def add_docs_to_collection(docs, metadata, ids, collection):
    collection.add(
        documents=docs,
        embeddings=get_embeddings(docs),
        metadatas=metadata,
        ids=ids
    )
    return collection