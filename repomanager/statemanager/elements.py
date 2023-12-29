import click
import os
import json
import pickle
import logging
from prompts.general import PROMPT_TO_EXPLAIN_CODE, PROMPT_TO_EXTRACT_INFO_FROM_CODE
from standard.extract import element_file_iterator, get_code, get_classname_classmethods
from error.graph import check_graph_elements
from llms.completion import get_llm, check_and_generate_explanation
import datetime
from llms.parse import parse_tripets
from graph.actions import add_triplets
import ast

# TODO: Make sure that the triplets don't contain information related to the function-calls, because they have
# already been added to the graph
# [('store_data', 'chunker.py', {'type': 'function'}),
#  ('store_data', 'final_chunks', {'type': 'function-call'}),
#  ('store_data', 'chunking_pipeline', {'type': 'function-call'}),
#  ('store_data', 'education_experience', {'type': 'EXTERNAL_DEPENDENCY'}),
#  ('store_data', 'final_chunks_0', {'type': 'EXTERNAL_DEPENDENCY'}),
#  ('store_data', 'filename', {'type': 'UNKNOWN'}),
#  ('store_data', 'input_1', {'type': 'UNKNOWN'}),
#  ('store_data', 'json.dump', {'type': 'UNKNOWN'}),
#  ('store_data', 'education_experience_0', {'type': 'REQUIRED_TYPE'}),
#  ('store_data', 'a filename', {'type': 'REQUIRED_TYPE'})]

logging.basicConfig(level=logging.INFO)

repo_map = json.load(open('./repo_map.json'))
llm = get_llm(max_tokens=256)

@click.command()
@click.argument('repo_name')
def update_elements(repo_name):
    
    repo_id = repo_map[f'{repo_name}']

    # if it doesn't exist, echo error
    if not os.path.exists(os.path.join('state', repo_id, 'state_0.pkl')):
        print('Error: state_0.pkl does not exist')
        return
    
    with open(os.path.join('state', repo_id, 'state_0.pkl'), 'rb') as f:
        G = pickle.load(f)
        
    elements_folder = os.path.join('state', repo_id, 'elements')

    temp_dict = element_file_iterator(elements_folder)

    for file in temp_dict.keys():

        code_snippet, codelines, asttree = get_code(file, elements_folder)

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

        # if the node doesn't have an info, generate one
        # TODO: the info this way is only updated once, to update it again, we need to pass an argument to command and use it to
        # run the code again
            
        #===============================================================================================================
        # comment this section out for now, as it is not needed
        #===============================================================================================================

        # if not G.nodes[temp_dict[file]['name']].get('info'):
        #     i = 0
        #     while i < 2:
        #         try:
        #             # if temp_dict[file]['type'] == 'class':
        #             #     code_snippet = _code
        #             info_prompt = PROMPT_TO_EXTRACT_INFO_FROM_CODE.format(code=code_snippet)
        #             info = llm.complete(info_prompt).text
        #             click.echo(click.style(info, fg='green'))
        #             triplet_strings = info.split('\n')
        #             triplets = parse_tripets(triplet_strings)
        #             G.nodes[temp_dict[file]['name']]['info'] = {
        #                 'generated': False,
        #                 'date_modified': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        #                 'n_info_edges': 0,
        #             }
        #             G = add_triplets(G, temp_dict[file]['name'], triplets)
        #             break
        #         except Exception as e:
        #             logging.debug(e)
        #             i += 1
        #             continue
        #     if i == 2:
        #         logging.info(f'Error: could not generate info for {temp_dict[file]["name"]} of type {temp_dict[file]["type"]}')
        #         continue
        #     # update the node metadata with the info
        #     G.nodes[temp_dict[file]['name']]['info']['generated'] = True
        #     # update the node metadata with the date_modified
        #     G.nodes[temp_dict[file]['name']]['info']['date_modified'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # # save the graph as a pickle file
        # with open(os.path.join('state', repo_id, 'state_0.pkl'), 'wb') as f:
        #     pickle.dump(G, f)
        
        # logging.info(f'Updated {temp_dict[file]["name"]} of type {temp_dict[file]["type"]}')

    # print(G.nodes(data=True))
    # print(G.edges(data=True))
    # # if the og_file_name is not in the graph, echo error
    # if not G.has_node(og_file_name):
    #     print(f'Error: {og_file_name} does not exist in the graph')
    #     return
        
if __name__ == '__main__':
    update_elements()