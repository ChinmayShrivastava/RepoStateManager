import ast
import click
import os
import shutil
import json

repo_map = json.load(open('./repo_map.json'))

@click.command()
@click.argument('repo_name')
def extract_elements_from_python_file(repo_name):

    repo_id = repo_map[f'{repo_name}']

    with open(os.path.join('data/flattened', repo_id, 'directory.txt'), 'r') as f:
        filenames = f.readlines()

    for filename in filenames:

        filename = filename.strip()
        filename = filename.replace('/', '@@')

        if filename.split('.')[-1] != 'py':
            continue

        filepath = os.path.join('data/flattened', repo_id, 'files/', filename)
        try:
            with open(filepath, 'r') as f:
                # read the code
                code = f.read()
                # take the cursor to the beginning of the file
                f.seek(0)
                # read the lines of the file
                codelines = f.readlines()
        except:
            continue

        tree = ast.parse(code)
    
        functions = [(node.name, node.lineno, node.end_lineno) for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
        imports = [node.names[0].name for node in ast.walk(tree) if isinstance(node, ast.Import)]
        import_froms = [node.module for node in ast.walk(tree) if isinstance(node, ast.ImportFrom)]
        classes = [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
        # class_methods = {
        #     class_.name: [(node.name, node.lineno, node.end_lineno) for node in ast.walk(class_) if isinstance(node, ast.FunctionDef)] for class_ in classes
        # }
        # classe name, start line, end line
        classes = [(class_.name, class_.lineno, class_.end_lineno) for class_ in classes]

        # remove the functions if they are in the classes
        for class_ in classes:
            functions = [function for function in functions if function[1] < class_[1] or function[2] > class_[2]]

        # make a state/{repo_id}/tree folder, if it doesn't exist
        if not os.path.exists(f'state/{repo_id}/tree'):
            os.makedirs(f'state/{repo_id}/tree')

        with open(f'state/{repo_id}/tree/{filename}.json', 'w') as f:
            json.dump({
                "functions": [function[0] for function in functions],
                "imports": imports,
                "import_froms": import_froms,
                "classes": [class_[0] for class_ in classes],
            }, f)

        # make a state/{repo_id}/elements/{filename} folder, if it doesn't exist
        if not os.path.exists(f'state/{repo_id}/elements'):
            os.makedirs(f'state/{repo_id}/elements')

        # for the elements in function and the code in code, create a file in state/{repo_id}/elements/{filename} with the code
        for i, function in enumerate(functions):
            with open(f'state/{repo_id}/elements/{filename[0:-3]}!!function!!{i}!!{function[0]}.py', 'w') as f:
                f.writelines(codelines[function[1]-1:function[2]])

        # for the elements in classes and the code in code, create a file in state/{repo_id}/elements/{filename} with the code
        for i, class_ in enumerate(classes):
            with open(f'state/{repo_id}/elements/{filename[0:-3]}!!class!!{i}!!{class_[0]}.py', 'w') as f:
                f.writelines(codelines[class_[1]-1:class_[2]])

if __name__ == '__main__':
    extract_elements_from_python_file()
