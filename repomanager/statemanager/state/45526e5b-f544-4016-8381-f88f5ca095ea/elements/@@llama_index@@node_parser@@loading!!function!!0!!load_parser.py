def load_parser(
    data: dict,
) -> NodeParser:
    if isinstance(data, NodeParser):
        return data
    parser_name = data.get("class_name", None)
    if parser_name is None:
        raise ValueError("Parser loading requires a class_name")

    if parser_name not in all_node_parsers:
        raise ValueError(f"Invalid parser name: {parser_name}")
    else:
        return all_node_parsers[parser_name].from_dict(data)
