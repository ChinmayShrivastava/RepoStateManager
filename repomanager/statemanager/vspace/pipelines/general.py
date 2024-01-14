from prompts.retrieval_prompts import VECTOR_SEARCH_FOR_CLASS
from defaults.vsearch import DISTANCE_THRESHOLD_pinecone, DIFFERENCE_THRESHOLD_pinecone

def get_initial_information(query: str, graph, explanations) -> str:
    """takes in a query and try to logically reason for relevant context"""
    relevant_class, names = get_relevant_class(query, explanations)
    if relevant_class is not None:
        # get the code for the class element
        # element = graph.G.nodes[relevant_class]
        element = graph.get_node_metadata(relevant_class)
        code = graph.get_code(element, element['elementname'])
        edges = graph.get_edges_by_type(element)
        # parent classes
        parent_classes = list(set([edge.start_node for edge in edges.edges if edge.start_node != element['name']]))
        # parentclass methods
        parent_class_methods = []
        for parentclass in parent_classes:
            parent_class_methods += list(set([edge.end_node for edge in edges.edges if edge.start_node == parentclass]))
        _string = "The following is some context for the class {class_name}.\n"
        _string += "This is a code outline of the class {class_name}:\n\n"
        _string += code
        _string += "\n\n"
        _string += "The class inherits from the following classes:\n\n"
        for parentclass in parent_classes:
            _string += f"class:{parentclass}\n"
            _string += "This parent class has the following methods:\n\n"
            for method in parent_class_methods:
                _string += f"method:{method}\n"
        return _string.format(class_name=relevant_class)
    else:
        _string = "The following are the classes that might be relevant:\n"
        _string += "----------\n"
        for name in names:
            _string += f"class:{name}\n"
        _string += "----------\n"
        _string += "\n"
        _string += "Please select one of the classes above and request for more information. Use the get_code tool with the class name."
        return _string

def get_relevant_class(query: str, explanations) -> str:
    """takes in a query and try to logically reason for relevant class"""
    _prompt = VECTOR_SEARCH_FOR_CLASS.format(query=query)
    results = explanations.search_all(_prompt, type="class", top_k=5)
    # for chromadb
    # names = results['ids'][0]
    # distances = results['distances'][0]
    # for pinecone
    matches = results['matches']
    names = [match['id'] for match in matches]
    distances = [match['score'] for match in matches]
    zipped = zip(names, distances)
    # filter out the ones that are too far away
    filtered = list(filter(lambda x: x[1] > DISTANCE_THRESHOLD_pinecone, zipped))
    # if the len is 0, return None
    if len(filtered) == 0:
        return None, names
    elif len(filtered) == 1:
        return filtered[0][0], names
    elif len(filtered) > 1:
        # if the difference between the first and second is too small, return None
        if filtered[0][1] - filtered[1][1] < DIFFERENCE_THRESHOLD_pinecone:
            return None, names
        else:
            return filtered[0][0], names