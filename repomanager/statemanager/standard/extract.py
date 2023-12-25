import ast

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
    assert filename[0] == '/' and filename[-3:] == '.py'
    # read the file from data/flattened/repo_id/files+filename and get the code
    with open(f'data/flattened/{repo_id}/files'+filename, 'r') as f:
        code = f.read()
    # get the imports and the global variables
    return remove_functions_and_classes(code)

def remove_functions_and_classes(code):
    module = ast.parse(code)
    new_body = [node for node in module.body if not isinstance(node, (ast.FunctionDef, ast.ClassDef))]
    module.body = new_body
    return ast.unparse(module)