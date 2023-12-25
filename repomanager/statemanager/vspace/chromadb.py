import os
from chromadb import PersistentClient, HttpClient
from chromadb.utils import embedding_functions
from dotenv import load_dotenv
load_dotenv()
import click

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