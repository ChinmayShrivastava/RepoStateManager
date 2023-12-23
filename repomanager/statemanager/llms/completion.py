from llama_index.llms import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

def get_llm(model='gpt-3.5-turbo'):
    return OpenAI(model=model)