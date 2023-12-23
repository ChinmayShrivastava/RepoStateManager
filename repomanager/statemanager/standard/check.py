import re

def is_local(path, repoid):
    # if path is of the type something.something else
    if re.match(r'.*\..*', path):
        list_of_nodes = [x for x in path.split('.') if x != '']
    # if the path is of the type something/something else
    elif re.match(r'.*/.*', path):
        list_of_nodes = [x for x in path.split('/') if x != '']
    else:
        list_of_nodes = [path]
    _path = '/'.join(list_of_nodes)
    # load the directory.txt file inder data/repoid
    with open('data/flattened/' + repoid + '/directory.txt', 'r') as f:
        lines = f.readlines()
        lines = [x.strip() for x in lines]
    for line in lines:
        if _path in line:
            return True
    return False