import ast
import click
import os
import shutil
import json
import astor

repo_map = json.load(open('./repo_map.json'))

@click.command()
@click.argument('repo_name')
def extract_elements_from_python_file(repo_name):

    repo_id = repo_map[f'{repo_name}']

    with open(os.path.join('data/flattened', repo_id, 'directory.txt'), 'r') as f:
        filenames = f.readlines()

    # for each line in the file, create nodes to map directories, e.g. if line is a/b/c/d.txt, create nodes a, b, c, d.txt and edges a->b->c->d.txt
    for filename in filenames:

        filename = filename.strip()

        if filename.endswith('.py'):

            filename = f'data_{repo_id}_'+filename.replace('/', '_')

            with open(f'data/flattened/{repo_id}/files/{filename}', 'r') as f:
                code = f.read()

            tree = ast.parse(code)
        
            functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
            imports = [node.names[0].name for node in ast.walk(tree) if isinstance(node, ast.Import)]
            import_froms = [node.module for node in ast.walk(tree) if isinstance(node, ast.ImportFrom)]

            # make a state/{repo_id}/tree folder, if it doesn't exist
            if not os.path.exists(f'state/{repo_id}/tree'):
                os.makedirs(f'state/{repo_id}/tree')

            with open(f'state/{repo_id}/tree/{filename}.json', 'w') as f:
                json.dump({
                    "functions": functions,
                    "imports": imports,
                    "import_froms": import_froms
                }, f)

            # make a state/{repo_id}/elements/{filename} folder, if it doesn't exist
            if not os.path.exists(f'state/{repo_id}/elements'):
                os.makedirs(f'state/{repo_id}/elements')

            functions = [(node.lineno, node.end_lineno) for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
            imports = [(node.lineno, node.end_lineno) for node in ast.walk(tree) if isinstance(node, ast.Import)]
            import_froms = [(node.lineno, node.end_lineno) for node in ast.walk(tree) if isinstance(node, ast.ImportFrom)]

            print(functions)
            print(imports)
            print(import_froms)

            with open(f'data/{repo_id}{filename}', 'r') as f:
                codelines = f.readlines()

            # for the elements in function and the code in code, create a file in state/{repo_id}/elements/{filename} with the code
            for function in functions:
                with open(f'state/{repo_id}/elements/{filename}_{function[0]}_{function[1]}.py', 'w') as f0:
                    f0.writelines(codelines[function[0]-1:function[1]])

if __name__ == '__main__':
    extract_elements_from_python_file()
