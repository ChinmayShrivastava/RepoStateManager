import click
import os
import json
import pickle
import logging
# from prompts.general import PROMPT_TO_EXPLAIN_CODE, PROMPT_TO_EXTRACT_INFO_FROM_CODE
# from standard.extract import element_file_iterator, get_element_code, get_classname_classmethods
# from error.graph import check_graph_elements
# from llms.completion import get_llm, check_and_generate_explanation
import datetime
# from llms.parse import parse_tripets
# from graph.actions import add_triplets
import ast

# llm = get_llm(max_tokens=256)
def update_elements(state_loc, llm):
    
    with open(state_loc, 'rb') as f:
        G = pickle.load(f)
        
    # elements_folder = os.path.join('state', repo_id, 'elements')

    temp_dict = element_file_iterator(elements_folder)

    for file in temp_dict.keys():

        code_snippet, codelines, asttree = get_element_code(file, elements_folder)

        if temp_dict[file]['type'] != 'class':
            click.echo(f'Updating {temp_dict[file]["name"]} of type {temp_dict[file]["type"]}')
            if not check_graph_elements(G, temp_dict[file]['og_file_name'], temp_dict[file]['name']):
                return
            G = check_and_generate_explanation(G, temp_dict[file]['name'], code_snippet, llm)
        else:
            class_name, class_methods = get_classname_classmethods(asttree, codelines)
            for method_name, method_code in class_methods:
                code_snippet = code_snippet.replace(method_code, 'Method Goes Here: '+ method_name)
            if not check_graph_elements(G, temp_dict[file]['og_file_name'], class_name):
                return
            G = check_and_generate_explanation(G, class_name, code_snippet, llm)
            # add explanation for each method
            for method_name, method_code in class_methods:
                if not G.has_node(method_name):
                    # if the name node is not in the graph, echo error
                    logging.info(f'Error: {method_name} of type {temp_dict[file]["type"]} does not exist in the graph')
                    return
                G = check_and_generate_explanation(G, method_name, method_code, llm)
                # add edge from class to method
                if not G.has_edge(class_name, method_name):
                    G.add_edge(class_name, method_name, type='class-method')

        # save the graph as a pickle file
        with open(os.path.join('state', repo_id, 'state_0.pkl'), 'wb') as f:
            pickle.dump(G, f)