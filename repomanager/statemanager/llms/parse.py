def parse_tripets(list_of_trilet_strings):
    '''
    Each of the triplets is a string of the form: (subject, predicate, object)
    This function parses the triplets as a list of tuples of the form: (subject, predicate, object)
    Returns the list of tuples
    '''
    list_of_trilet_tuples = []
    for trilet_string in list_of_trilet_strings:
        trilet_tuple = parse_trilet(trilet_string)
        list_of_trilet_tuples.append(trilet_tuple)
    # make sure that the list is unique
    list_of_trilet_tuples = list(set(list_of_trilet_tuples))
    return list_of_trilet_tuples

def parse_trilet(trilet_string):
    '''
    Each of the triplets is a string of the form: (subject, predicate, object)
    This function parses the triplet as a tuple of the form: (subject, predicate, object)
    Returns the tuple
    '''
    trilet_tuple = ()
    trilet_string = trilet_string.strip()
    # remove the brackets
    trilet_string = trilet_string[1:-1]
    # split by commas
    trilet_string = trilet_string.split(',')
    trilet_string = [x.strip() for x in trilet_string]
    # remove empty strings
    trilet_string = [x for x in trilet_string if x != '']
    # make tuple
    trilet_tuple = tuple(trilet_string)
    return trilet_tuple