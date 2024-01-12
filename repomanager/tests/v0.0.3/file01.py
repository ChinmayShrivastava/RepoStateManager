from statemanager.prompts.retrieval_prompts import VECTOR_SEARCH_FOR_CLASS

DISTANCE_THRESHOLD = 0.19
DIFFERENCE_THRESHOLD = 0.015

def get_initial_information(query: str, graph, explanations, triplets) -> str:
    """takes in a query and try to logically reason for relevant context"""
    relevant_class, names = get_relevant_class(query, explanations)
    if relevant_class is not None:
        # get the code for the class element
        element = graph.G.nodes[relevant_class]
        # code = graph.get_code(element, element['elementname'])
        edges = graph.get_edges_by_type(element)
        _string = "The following is some context for the class {class_name}.\n"
        _string += "The class {class_name} has the following properties:\n\n"
        for edge in edges.edges:
            _string += f"{edge.start_node} : {edge.metadata['type']} : {edge.end_node}\n"
        return _string.format(class_name=relevant_class)
    else:
        _string = "The following are the classes that might be relevant:\n\n"
        for name in names:
            _string += f"class:{name}\n"
        _string += "\n\n"
        _string += "Please select one of the classes above and request for more information"
        return _string


def get_relevant_class(query: str, explanations) -> str:
    """takes in a query and try to logically reason for relevant class"""
    _prompt = VECTOR_SEARCH_FOR_CLASS.format(query=query)
    results = explanations.search_all(_prompt, type="class", top_k=3)
    names = results['ids'][0]
    distances = results['distances'][0]
    zipped = zip(names, distances)
    # filter out the ones that are too far away
    filtered = list(filter(lambda x: x[1] < DISTANCE_THRESHOLD, zipped))
    # if the len is 0, return None
    if len(filtered) == 0:
        return None
    elif len(filtered) == 1:
        return filtered[0][0]
    elif len(filtered) > 1:
        # if the difference between the first and second is too small, return None
        if filtered[1][1] - filtered[0][1] < DIFFERENCE_THRESHOLD:
            return None, names
        else:
            return filtered[0][0], names