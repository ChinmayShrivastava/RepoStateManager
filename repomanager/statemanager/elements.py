import click
import os
import json
import pickle
import logging
from prompts.general import PROMPT_TO_EXPLAIN_CODE, PROMPT_TO_EXTRACT_INFO_FROM_CODE
from llms.completion import get_llm
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

    # go through the state/repo_id/elements folder and read all the files
    elements_folder = os.path.join('state', repo_id, 'elements')
    files = os.listdir(elements_folder)

    temp_dict = {}

    # for each file, read the file and update the graph
    for file in files:

        filename = file.split('.')[0]
        eles = filename.split('!!')
        # TODO: make sure that if the file is a directory, then it is accounted for
        og_file_name = eles[0].split('@@')[-1]+'.py'
        ele_type = eles[1]
        ele_index = eles[2]
        ele_name = eles[3]

        temp_dict[file] = {
            'name': ele_name,
            'type': ele_type,
            'index': ele_index,
            'og_file_name': og_file_name,
        }
    
    logging.info(f'extracted element info from {len(temp_dict)} files')

    for file in temp_dict.keys():
        if temp_dict[file]['type'] != 'class':
            click.echo(f'Updating {temp_dict[file]["name"]} of type {temp_dict[file]["type"]}')
            if not G.has_node(temp_dict[file]['og_file_name']):
                # if the og_file_name is not in the graph, echo error
                logging.info('Error: {} does not exist in the graph'.format(temp_dict[file]['og_file_name']))
                return
            if not G.has_node(temp_dict[file]['name']):
                # if the name node is not in the graph, echo error
                logging.info(f'Error: {temp_dict[file]["name"]} of type {temp_dict[file]["type"]} does not exist in the graph')
                return
            if not G.has_edge(temp_dict[file]['og_file_name'], temp_dict[file]['name']):
                # if the edge does not exist, echo error
                logging.info('Error: edge from {} to {} does not exist in the graph'.format(temp_dict[file]['og_file_name'], temp_dict[file]['name']))
            # get code snippet
            code_snippet = open(os.path.join(elements_folder, file)).read()
            # if the node doesn't have an explanation, generate one
            if not G.nodes[temp_dict[file]['name']].get('explanation'):
                logging.info(f'Generating explanation for {temp_dict[file]["name"]} of type {temp_dict[file]["type"]}')
                explanation_prompt = PROMPT_TO_EXPLAIN_CODE.format(code=code_snippet)
                explanation = llm.complete(explanation_prompt).text
                # update the node metadata with the explanation
                G.nodes[temp_dict[file]['name']]['explanation'] = explanation
        else:
            # read the class file, parst it into an ast tree
            _code = open(os.path.join(elements_folder, file)).read()
            codelines = open(os.path.join(elements_folder, file)).read().split('\n')
            while True:
                try:
                    asttree = ast.parse(_code)
                    break
                except IndentationError:
                    # remove the first 4 spaces from each line
                    _code = '\n'.join([line[4:] for line in _code.split('\n')])
                    codelines = _code.split('\n')
                    continue
            # get the class name
            class_name = [node.name for node in ast.walk(asttree) if isinstance(node, ast.ClassDef)][0]
            # get the class method names, start line and end line
            class_methods = [(node.name, '\n'.join(codelines[node.lineno-1:node.end_lineno])) for node in ast.walk(asttree) if isinstance(node, ast.FunctionDef)]
            # method_codes = [_code[lineno-1:end_lineno] for _, lineno, end_lineno in class_methods]
            # replace the medhod code with the method name in the class code
            for method_name, method_code in class_methods:
                _code = _code.replace(method_code, 'Method Goes Here: '+method_name)
            if not G.has_node(temp_dict[file]['og_file_name']):
                # if the og_file_name is not in the graph, echo error
                logging.info('Error: {} does not exist in the graph'.format(temp_dict[file]['og_file_name']))
                return
            if not G.has_node(class_name):
                # if the name node is not in the graph, echo error
                logging.info(f'Error: {class_name} of type {temp_dict[file]["type"]} does not exist in the graph')
                return
            if not G.has_edge(temp_dict[file]['og_file_name'], class_name):
                # if the edge does not exist, echo error
                logging.info('Error: edge from {} to {} does not exist in the graph'.format(temp_dict[file]['og_file_name'], class_name))
            # if the node doesn't have an explanation, generate one
            if not G.nodes[class_name].get('explanation'):
                logging.info(f'Generating explanation for {class_name} of type {temp_dict[file]["type"]}')
                explanation_prompt = PROMPT_TO_EXPLAIN_CODE.format(code=_code)
                explanation = llm.complete(explanation_prompt).text
                # update the node metadata with the explanation
                G.nodes[class_name]['explanation'] = explanation
            # add explanation for each method
            for method_name, method_code in class_methods:
                if not G.has_node(method_name):
                    # if the name node is not in the graph, echo error
                    logging.info(f'Error: {method_name} of type {temp_dict[file]["type"]} does not exist in the graph')
                    return
                if not G.nodes[method_name].get('explanation'):
                    logging.info(f'Generating explanation for {method_name} of type {temp_dict[file]["type"]}')
                    explanation_prompt = PROMPT_TO_EXPLAIN_CODE.format(code=method_code)
                    explanation = llm.complete(explanation_prompt).text
                    # update the node metadata with the explanation
                    G.nodes[method_name]['explanation'] = explanation
                # add edge from class to method
                if not G.has_edge(class_name, method_name):
                    G.add_edge(class_name, method_name, type='class-method')

        # save the graph as a pickle file
        with open(os.path.join('state', repo_id, 'state_0.pkl'), 'wb') as f:
            pickle.dump(G, f)

        # if the node doesn't have an info, generate one
        # TODO: the info this way is only updated once, to update it again, we need to pass an argument to command and use it to
        # run the code again
        if not G.nodes[temp_dict[file]['name']].get('info'):
            i = 0
            while i < 2:
                try:
                    if temp_dict[file]['type'] == 'class':
                        code_snippet = _code
                    info_prompt = PROMPT_TO_EXTRACT_INFO_FROM_CODE.format(code=code_snippet)
                    info = llm.complete(info_prompt).text
                    click.echo(click.style(info, fg='green'))
                    triplet_strings = info.split('\n')
                    triplets = parse_tripets(triplet_strings)
                    G.nodes[temp_dict[file]['name']]['info'] = {
                        'generated': False,
                        'date_modified': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'n_info_edges': 0,
                    }
                    G = add_triplets(G, temp_dict[file]['name'], triplets)
                    break
                except Exception as e:
                    logging.debug(e)
                    i += 1
                    continue
            if i == 2:
                logging.info(f'Error: could not generate info for {temp_dict[file]["name"]} of type {temp_dict[file]["type"]}')
                continue
            # update the node metadata with the info
            G.nodes[temp_dict[file]['name']]['info']['generated'] = True
            # update the node metadata with the date_modified
            G.nodes[temp_dict[file]['name']]['info']['date_modified'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # save the graph as a pickle file
        with open(os.path.join('state', repo_id, 'state_0.pkl'), 'wb') as f:
            pickle.dump(G, f)
        
        logging.info(f'Updated {temp_dict[file]["name"]} of type {temp_dict[file]["type"]}')

    print(G.nodes(data=True))
    print(G.edges(data=True))
    # # if the og_file_name is not in the graph, echo error
    # if not G.has_node(og_file_name):
    #     print(f'Error: {og_file_name} does not exist in the graph')
    #     return
        
if __name__ == '__main__':
    update_elements()