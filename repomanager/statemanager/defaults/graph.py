from typing import List

LEVEL_ONE_INFORMATION = {
    "function": ['*'],
    "class": ['e:parent-class->n:class->e:class-method->n:method', 'e:class-method->n:method'],
}

def search_parser(_string: str) -> List[str]:
    """Takes in a search string and returns a list of search terms"""
    if _string == '*':
        return [{
            'type': 'e',
            'type-name': 'aLL',
        }]
    else:
        _string = _string.split('->')
        _string = [i.split(':') for i in _string]
        _string = [{
            'type': _string[i][0],
            'type-name': _string[i][1],
        } for i in range(len(_string))]
        return _string
    
def parsed_info(type_name: str) -> List[List[dict]]:
    """Takes in a type and type name and returns a list of edges"""
    strings = LEVEL_ONE_INFORMATION[type_name]
    return [search_parser(i) for i in strings]
    
if __name__ == '__main__':
    print(parsed_info('function'))