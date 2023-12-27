from llama_index.llms import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

def get_llm(model='gpt-3.5-turbo', max_tokens=756):
    return OpenAI(model=model, max_tokens=max_tokens)