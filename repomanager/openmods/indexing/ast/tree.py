import ast
import os
import json
from type import Node

def element_tree(tree_map, dir_map):

    treemap = {}

    # load the directory_map from the dir_map file
    with open(dir_map, 'r') as f:
        directory_map = json.load(f)

    for idx, filename in enumerate(directory_map):

        filename = filename.strip()

        if filename.split('.')[-1] != 'py':
            continue
        
        try:
            with open(filename, 'r') as f:
                # read the code
                code = f.read()
                # take the cursor to the beginning of the file
                f.seek(0)
                # read the lines of the file
                codelines = f.readlines()
        except:
            continue

        tree = ast.parse(code)
    
        functions = [Node(
            name=node.name, 
            type='function',
            file_name=filename,
            code_start_line=node.lineno,
            code_end_line=node.end_lineno,
            ) for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
        classes = [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
        classes = [Node(
            name=_class.name, 
            type='class',
            file_name=filename,
            code_start_line=_class.lineno,
            code_end_line=_class.end_lineno,
            ) for _class in classes]
        # remove the functions if they are in the classes
        for _class in classes:
            # functions = [function for function in functions if function[1] < _class[1] or function[2] > _class[2]]
            functions = [function for function in functions if function.code_start_line < _class.code_start_line or function.code_end_line > _class.code_end_line]

        # treemap[idx] = {
        #     'filename': filename,
        #     'functions': functions,
        #     'classes': classes,
        # }
        treemap[idx] = {
            'filename': filename,
            'functions': [function.model_dump() for function in functions],
            'classes': [class_.model_dump() for class_ in classes],
        }

    # write the treemap to the file
    with open(tree_map, 'w') as f:
        json.dump(treemap, f, indent=4)

    return treemap