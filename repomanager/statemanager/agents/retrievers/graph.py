import ast

def get_code(nx_node, repo_id, elementname):
    """Takes in one node fron networkx and returns the code associated with it."""
    type_ = nx_node['type']
    name = nx_node['name']
    with open(f"../state/{repo_id}/elements/{elementname}", "r") as f:
        _code = f.read()
    return function_dispatch_type['get_code'][type_](name, _code)

def get_function_code(name, code):
    return code

def get_class_breakdown(code):
    # read the class file, parst it into an ast tree
    codelines = code.split('\n')
    while True:
        try:
            asttree = ast.parse(code)
            break
        except IndentationError:
            # remove the first 4 spaces from each line
            code = '\n'.join([line[4:] for line in code.split('\n')])
            codelines = code.split('\n')
    # get the class name
    class_name = [node.name for node in ast.walk(asttree) if isinstance(node, ast.ClassDef)][0]
    # get the class method names, start line and end line
    class_methods = [(node.name, '\n'.join(codelines[node.lineno-1:node.end_lineno])) for node in ast.walk(asttree) if isinstance(node, ast.FunctionDef)]
    return class_name, class_methods

def get_class_code(name, code):
    class_name, class_methods = get_class_breakdown(code)
    for method_name, method_code in class_methods:
        code = code.replace(method_code, 'Method Goes Here -> Method name is \'' + method_name + '\'')
    return code

def get_method_code(name, code):
    class_name, class_methods = get_class_breakdown(code)
    for method_name, method_code in class_methods:
        if method_name == name:
            return method_code
    return 'Method not found'

function_dispatch_type = {
    'get_code': {
        'function': get_function_code,
        'class': get_class_code,
        'method': get_method_code,
    }
}