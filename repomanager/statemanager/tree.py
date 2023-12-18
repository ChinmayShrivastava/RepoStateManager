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

        if filename.split('.')[-1] != 'py':
            continue

        filepath = os.path.join('data/flattened', repo_id, 'files', filename[1:])
        with open(filepath, 'r') as f:
            # read the code
            code = f.read()
            # take the cursor to the beginning of the file
            f.seek(0)
            # read the lines of the file
            codelines = f.readlines()

        tree = ast.parse(code)
    
        functions = [(node.name, node.lineno, node.end_lineno) for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
        imports = [node.names[0].name for node in ast.walk(tree) if isinstance(node, ast.Import)]
        import_froms = [node.module for node in ast.walk(tree) if isinstance(node, ast.ImportFrom)]

        # make a state/{repo_id}/tree folder, if it doesn't exist
        if not os.path.exists(f'state/{repo_id}/tree'):
            os.makedirs(f'state/{repo_id}/tree')

        with open(f'state/{repo_id}/tree/{filename}.json', 'w') as f:
            json.dump({
                "functions": [function[0] for function in functions],
                "imports": imports,
                "import_froms": import_froms
            }, f)

        # make a state/{repo_id}/elements/{filename} folder, if it doesn't exist
        if not os.path.exists(f'state/{repo_id}/elements'):
            os.makedirs(f'state/{repo_id}/elements')

        # for the elements in function and the code in code, create a file in state/{repo_id}/elements/{filename} with the code
        for i, function in enumerate(functions):
            with open(f'state/{repo_id}/elements/{filename[0:-3]}!!function!!{i}!!{function[0]}.py', 'w') as f:
                f.writelines(codelines[function[1]-1:function[2]])

if __name__ == '__main__':
    extract_elements_from_python_file()
