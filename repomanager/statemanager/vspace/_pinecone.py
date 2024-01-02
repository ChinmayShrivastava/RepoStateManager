import pinecone
import os
from dotenv import load_dotenv
load_dotenv()

def return_pinecone_index(index_name: str) -> pinecone.Index:
    """Takes in a collection name and returns the pinecone index associated with it"""
    pinecone.init(      
        api_key=os.environ['PINECONE_API_KEY'], 
        environment=os.environ['PINECONE_ENVIRONMENT']    
    )      
    index = pinecone.Index(os.environ['INDEX_NAME'])
    return index