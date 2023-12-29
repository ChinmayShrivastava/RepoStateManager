import ast
import os
import logging

# # go through the state/repo_id/elements folder and read all the files
    # elements_folder = os.path.join('state', repo_id, 'elements')
    # files = os.listdir(elements_folder)

    # temp_dict = {}

    # # for each file, read the file and update the graph
    # for file in files:

    #     filename = file.split('.')[0]
    #     eles = filename.split('!!')
    #     # TODO: make sure that if the file is a directory, then it is accounted for
    #     og_file_name = eles[0].split('@@')[-1]+'.py'
    #     ele_type = eles[1]
    #     ele_index = eles[2]
    #     ele_name = eles[3]

    #     temp_dict[file] = {
    #         'name': ele_name,
    #         'type': ele_type,
    #         'index': ele_index,
    #         'og_file_name': og_file_name,
    #     }

def element_file_iterator(elements_folder):
    
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

    return temp_dict

def get_element_code(file, elements_folder):
    code_snippet = open(os.path.join(elements_folder, file)).read()
    codelines = open(os.path.join(elements_folder, file)).read().split('\n')
    while True:
        try:
            asttree = ast.parse(code_snippet)
            break
        except IndentationError:
            # remove the first 4 spaces from each line
            code_snippet = '\n'.join([line[4:] for line in code_snippet.split('\n')])
            codelines = code_snippet.split('\n')
            continue
    return code_snippet, codelines, asttree

def get_imports(code):
    tree = ast.parse(code)
    imports = []
    importfroms = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            importfroms.append(([x for x in node.module.split('.') if len(x)!=0], [alias.name for alias in node.names]))
    return imports, importfroms

# gets the imports and the global variables
def get_imports_and_g_variables(filename, repo_id):
    # assert that the file name starts with /
    assert filename[-3:] == '.py'
    # read the file from data/flattened/repo_id/files+filename and get the code
    with open(f'data/flattened/{repo_id}/files/'+filename, 'r') as f:
        code = f.read()
    # get the imports and the global variables
    return remove_functions_and_classes(code)

def remove_functions_and_classes(code):
    module = ast.parse(code)
    new_body = [node for node in module.body if not isinstance(node, (ast.FunctionDef, ast.ClassDef))]
    module.body = new_body
    return ast.unparse(module)

def get_classname_classmethods(asttree, codelines):
    # get the class name
    class_name = [node.name for node in ast.walk(asttree) if isinstance(node, ast.ClassDef)][0]
    # get the class method names, start line and end line
    class_methods = [(node.name, '\n'.join(codelines[node.lineno-1:node.end_lineno])) for node in ast.walk(asttree) if isinstance(node, ast.FunctionDef)]
    return class_name, class_methods

def directory_file_iterator(repo_id):

    with open(os.path.join('data/flattened', repo_id, 'directory.txt'), 'r') as f:
        filenames = f.readlines()
        filenames = [x.strip() for x in filenames]

    files_to_return = []

    for filename in filenames:
        filename = filename.strip()
        if filename.split('.')[-1] != 'py':
            continue
        filepath = os.path.join('data/flattened', repo_id, 'files/', filename.replace('/', '@@'))
        files_to_return.append(filepath)
    
    logging.info(f'extracted {len(files_to_return)} files from directory.txt')

    return files_to_return

def directory_code_iterator(repo_id):
    filepaths = directory_file_iterator(repo_id)
    for filepath in filepaths:     
        with open(filepath, 'r') as f:
            # read the code
            code = f.read()
        yield code, filepath