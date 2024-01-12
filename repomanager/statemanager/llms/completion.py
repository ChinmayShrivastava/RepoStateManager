from llama_index.llms import OpenAI
from dotenv import load_dotenv
import os
import logging

load_dotenv()

def get_llm(model='gpt-3.5-turbo', max_tokens=756):
    return OpenAI(model=model, max_tokens=max_tokens)

def check_and_generate_explanation(G, node_name, code_snippet, llm):
    from prompts.general import PROMPT_TO_EXPLAIN_CODE
    if not G.nodes[node_name].get('explanation'):
        logging.info(f'Generating explanation for {node_name}')
        explanation_prompt = PROMPT_TO_EXPLAIN_CODE.format(code=code_snippet)
        explanation = llm.complete(explanation_prompt).text
        # update the node metadata with the explanation
        G.nodes[node_name]['explanation'] = explanation
    return G